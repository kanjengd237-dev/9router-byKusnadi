export default {
  id: "opencode",
  priority: 40,
  hasFree: true,
  alias: "oc",
  uiAlias: "oc",
  display: {
    name: "OpenCode Free",
    icon: "terminal",
    color: "#E87040",
    textIcon: "OC",
  },
  category: "free",
  noAuth: true,
  transport: {
    baseUrl: "https://opencode.ai/v1/chat/completions",
    headers: {
      "x-opencode-client": "desktop",
    },
    noAuth: true,
  },
  models: [
    // Only this model is served by /zen/v1/responses; the rest stay on
    // /chat/completions, so the format is declared per-model, not per-provider.
    { id: "muse-spark-1.2-contributor-free", name: "Muse Spark 1.2 Contributor Free", targetFormat: "openai-responses" },
    { id: "deepseek-v4", name: "DeepSeek V4" },
    { id: "deepseek-v4-pro", name: "DeepSeek V4 Pro" },
    { id: "deepseek-chat", name: "DeepSeek Chat" },
  ],
  modelsFetcher: { url: "https://opencode.ai/v1/models", type: "opencode-free" },
  passthroughModels: true,
};
