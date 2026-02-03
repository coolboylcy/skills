#!/usr/bin/env python3
"""
Real-time dashboard - Monitor openclaw-optimizer performance.
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone

class Dashboard:
    def __init__(self, skill_path="~/.clawdbot/skills/openclaw-optimizer"):
        self.skill_path = Path(skill_path).expanduser()
        self.cost_state = self.skill_path / "state/cost-state.json"
        self.browser_lock = self.skill_path / "state/browser-lock.json"
        self.task_history = self.skill_path / "state/task-history.jsonl"
        self.budget_tracker = Path("~/.clawdbot/budget-tracker.json").expanduser()
        self.circuit_breaker = Path("~/.clawdbot/circuit-breaker.json").expanduser()
    
    def get_summary(self):
        """Get overall summary of optimizer performance."""
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "daily_spend": self.get_daily_spend(),
            "browser_status": self.get_browser_status(),
            "circuit_status": self.get_circuit_status(),
            "tasks_today": self.get_tasks_today(),
            "cost_by_task_type": self.get_cost_by_task_type()
        }
        return summary
    
    def get_daily_spend(self):
        """Get daily spending from cost-state and budget-tracker."""
        total = 0.0
        
        # From cost-state (optimizer tracked)
        if self.cost_state.exists():
            with open(self.cost_state) as f:
                state = json.load(f)
                total += state.get("daily_total", 0.0)
        
        # From budget-tracker (global)
        if self.budget_tracker.exists():
            with open(self.budget_tracker) as f:
                tracker = json.load(f)
                
                # Only count today
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                if tracker.get("date") == today:
                    total = tracker.get("total_cost", 0.0)
        
        return round(total, 2)
    
    def get_browser_status(self):
        """Get browser lock status."""
        if not self.browser_lock.exists():
            return {"locked": False}
        
        with open(self.browser_lock) as f:
            lock = json.load(f)
        
        lock_age = time.time() - lock["timestamp"]
        
        return {
            "locked": True,
            "agent": lock["agent_id"],
            "task": lock["task"][:50] + "..." if len(lock["task"]) > 50 else lock["task"],
            "steps": lock["steps"],
            "age_seconds": round(lock_age, 1),
            "is_stale": lock_age > 300
        }
    
    def get_circuit_status(self):
        """Get circuit breaker status."""
        if not self.circuit_breaker.exists():
            return {"open": False, "requests_hour": 0}
        
        with open(self.circuit_breaker) as f:
            state = json.load(f)
        
        # Count recent requests
        now = time.time()
        hour_ago = now - 3600
        recent = [r for r in state.get("requests", []) if r["timestamp"] > hour_ago]
        
        return {
            "open": state.get("circuit_open", False),
            "loop_detected": state.get("loop_detected", False),
            "requests_hour": len(recent)
        }
    
    def get_tasks_today(self):
        """Count tasks run today."""
        if not self.task_history.exists():
            return {"total": 0, "success": 0, "failed": 0}
        
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        total = 0
        success = 0
        
        with open(self.task_history) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                entry_date = datetime.fromisoformat(entry["iso"]).strftime("%Y-%m-%d")
                
                if entry_date == today:
                    total += 1
                    if entry["success"]:
                        success += 1
        
        return {
            "total": total,
            "success": success,
            "failed": total - success,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0
        }
    
    def get_cost_by_task_type(self):
        """Get cost breakdown by task type for today."""
        if not self.task_history.exists():
            return {}
        
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        costs = {}
        
        with open(self.task_history) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                entry_date = datetime.fromisoformat(entry["iso"]).strftime("%Y-%m-%d")
                
                if entry_date == today:
                    task_type = entry["task_type"]
                    cost = entry["cost"]
                    
                    if task_type not in costs:
                        costs[task_type] = {"runs": 0, "cost": 0.0}
                    
                    costs[task_type]["runs"] += 1
                    costs[task_type]["cost"] += cost
        
        # Round costs
        for task_type in costs:
            costs[task_type]["cost"] = round(costs[task_type]["cost"], 3)
        
        return costs
    
    def print_dashboard(self):
        """Print formatted dashboard."""
        summary = self.get_summary()
        
        print("=" * 60)
        print("🚀 OPENCLAW OPTIMIZER DASHBOARD")
        print("=" * 60)
        print(f"📅 {summary['timestamp'][:19]} UTC")
        print()
        
        # Daily spend
        daily = summary["daily_spend"]
        budget = 10.0
        percent = (daily / budget) * 100
        bar_length = 30
        filled = int((daily / budget) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"💰 Daily Spend: ${daily:.2f} / ${budget:.2f}")
        print(f"   [{bar}] {percent:.1f}%")
        print()
        
        # Tasks today
        tasks = summary["tasks_today"]
        print(f"📊 Tasks Today: {tasks['total']} runs")
        print(f"   ✅ Success: {tasks['success']} ({tasks['success_rate']}%)")
        print(f"   ❌ Failed: {tasks['failed']}")
        print()
        
        # Cost by task type
        if summary["cost_by_task_type"]:
            print("💵 Cost Breakdown:")
            for task_type, data in sorted(summary["cost_by_task_type"].items(), 
                                         key=lambda x: x[1]["cost"], reverse=True):
                print(f"   {task_type:20} {data['runs']:2} runs  ${data['cost']:.3f}")
            print()
        
        # Browser status
        browser = summary["browser_status"]
        if browser["locked"]:
            emoji = "⚠️ " if browser["is_stale"] else "🔒"
            print(f"{emoji} Browser: LOCKED")
            print(f"   Agent: {browser['agent']}")
            print(f"   Task: {browser['task']}")
            print(f"   Steps: {browser['steps']}/20")
            print(f"   Age: {browser['age_seconds']}s")
        else:
            print("🟢 Browser: AVAILABLE")
        print()
        
        # Circuit breaker
        circuit = summary["circuit_status"]
        if circuit["open"]:
            print("🔴 Circuit Breaker: OPEN")
            if circuit["loop_detected"]:
                print("   ⚠️  Loop detected!")
        else:
            print("🟢 Circuit Breaker: CLOSED")
        print(f"   Requests (1h): {circuit['requests_hour']}")
        print()
        
        print("=" * 60)

if __name__ == "__main__":
    import sys
    
    dash = Dashboard()
    
    if len(sys.argv) > 1 and sys.argv[1] == "json":
        # JSON output for programmatic use
        summary = dash.get_summary()
        print(json.dumps(summary, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "watch":
        # Watch mode - refresh every 5 seconds
        try:
            while True:
                import os
                os.system('clear' if os.name != 'nt' else 'cls')
                dash.print_dashboard()
                print("Refreshing in 5s... (Ctrl+C to stop)")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n\n✅ Stopped monitoring")
    else:
        # Single snapshot
        dash.print_dashboard()
