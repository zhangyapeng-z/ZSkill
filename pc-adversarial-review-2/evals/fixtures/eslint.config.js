// ESLint 配置（用于测试）
// 对抗性审查 skill 使用时会读取项目本地的 ESLint 配置
export default [
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "error",
      "no-console": "off",
      "no-eval": "error",
      "eqeqeq": "warn",
      "no-redeclare": "error",
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        require: "readonly",
        console: "readonly",
        process: "readonly",
        __dirname: "readonly",
      },
    },
  },
];
