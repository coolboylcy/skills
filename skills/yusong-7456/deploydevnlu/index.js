export default async function handler(context) {
  const message = context?.event?.text || "no message";

  context.log("Slack message:", message);

  return {
    text: `Deploy skill received message: ${message}`
  };
}