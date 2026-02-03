#!/usr/bin/env python3
"""
Scheduler - Wrap automations with preflight/execute/postflight pattern.
"""

import json
import sys
import subprocess
import time
from pathlib import Path

class AutomationScheduler:
    def __init__(self, skill_path="~/.clawdbot/skills/openclaw-optimizer"):
        self.skill_path = Path(skill_path).expanduser()
        self.scripts = self.skill_path / "scripts"
    
    def run(self, task_type: str, task_description: str, agent_id: str = "automation"):
        """
        Run automation with full preflight/execute/postflight cycle.
        """
        task_id = f"{task_type}_{int(time.time())}"
        start_time = time.time()
        
        print(f"🚀 Starting automation: {task_type}")
        print(f"Task ID: {task_id}")
        
        # ===== PREFLIGHT =====
        print("\n📋 PREFLIGHT")
        
        # 1. Classify task
        result = subprocess.run(
            [sys.executable, str(self.scripts / "router.py"), task_description],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return self._fail("Router failed", result.stderr)
        
        print("✅ Task classified")
        
        # 2. Get budget recommendation
        result = subprocess.run(
            [sys.executable, str(self.scripts / "telemetry.py"), "recommend", task_type],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Budget recommended from history")
            # Parse recommendation (simplified - in real use, parse JSON)
            budget_soft = 0.10
            budget_max = 0.20
        else:
            print("⚠️  No history - using default budgets")
            budget_soft = 0.10
            budget_max = 0.20
        
        # 3. Acquire browser lock (if needed)
        needs_browser = "browser" in task_description.lower() or "navigate" in task_description.lower()
        
        if needs_browser:
            result = subprocess.run(
                [sys.executable, str(self.scripts / "browser_governor.py"), "acquire", agent_id, task_description],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("❌ Browser locked - queuing not implemented yet")
                return self._fail("Browser locked", result.stdout)
            
            print("✅ Browser lock acquired")
        
        # 4. Start cost tracking
        result = subprocess.run(
            [sys.executable, str(self.scripts / "cost_guard.py"), "start", 
             task_id, str(budget_soft), str(budget_max), 
             "anthropic/claude-3-5-haiku-latest", "5000", "1000"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            if needs_browser:
                subprocess.run([sys.executable, str(self.scripts / "browser_governor.py"), "release"])
            return self._fail("Cost guard rejected task", result.stdout)
        
        print("✅ Cost tracking started")
        print(f"   Budget soft: ${budget_soft:.2f}")
        print(f"   Budget max: ${budget_max:.2f}")
        
        # ===== EXECUTE =====
        print("\n⚙️  EXECUTE")
        print("   [Actual task execution would happen here]")
        print("   This is where you'd call the LLM, run browser, etc.")
        
        # Simulate execution
        time.sleep(1)
        
        # Log some spending
        subprocess.run(
            [sys.executable, str(self.scripts / "cost_guard.py"), "log",
             task_id, "5000", "1000", "anthropic/claude-3-5-haiku-latest"],
            capture_output=True
        )
        
        # ===== POSTFLIGHT =====
        print("\n📊 POSTFLIGHT")
        
        # 1. Release browser lock
        if needs_browser:
            subprocess.run([sys.executable, str(self.scripts / "browser_governor.py"), "release"])
            print("✅ Browser lock released")
        
        # 2. Finish cost tracking
        result = subprocess.run(
            [sys.executable, str(self.scripts / "cost_guard.py"), "finish", task_id],
            capture_output=True,
            text=True
        )
        
        print("✅ Cost tracking finished")
        
        # 3. Log telemetry
        duration = time.time() - start_time
        subprocess.run(
            [sys.executable, str(self.scripts / "telemetry.py"), "log",
             task_type, "anthropic/claude-3-5-haiku-latest", "0", "5000", "1000", 
             "0.01", str(duration), "true"],
            capture_output=True
        )
        
        print("✅ Telemetry logged")
        
        print(f"\n✅ Automation completed in {duration:.1f}s")
        
        return {
            "success": True,
            "task_id": task_id,
            "duration": duration,
            "cost": 0.01  # Would be actual cost
        }
    
    def _fail(self, reason: str, details: str):
        """Handle failure."""
        print(f"\n❌ FAILED: {reason}")
        if details:
            print(f"Details: {details}")
        return {
            "success": False,
            "reason": reason,
            "details": details
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: scheduler.py <task_type> <task_description>")
        print("\nExample:")
        print("  scheduler.py twitter_reply 'Navigate twitter, find openclaw posts, reply with value'")
        sys.exit(1)
    
    task_type = sys.argv[1]
    task_description = " ".join(sys.argv[2:])
    
    scheduler = AutomationScheduler()
    result = scheduler.run(task_type, task_description)
    
    sys.exit(0 if result["success"] else 1)
