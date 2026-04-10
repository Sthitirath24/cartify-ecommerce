const { spawn } = require("child_process");
const path = require("path");

const projectRoot = __dirname;
const pythonCmd = process.env.PYTHON_CMD || "python";
const pythonArgs = ["app.py"];

const child = spawn(pythonCmd, pythonArgs, {
  cwd: projectRoot,
  stdio: "inherit",
  shell: true
});

child.on("error", (err) => {
  console.error("Failed to start Python app:", err.message);
  process.exit(1);
});

child.on("exit", (code) => {
  process.exit(code ?? 0);
});

process.on("SIGINT", () => {
  if (!child.killed) child.kill("SIGINT");
});

process.on("SIGTERM", () => {
  if (!child.killed) child.kill("SIGTERM");
});
