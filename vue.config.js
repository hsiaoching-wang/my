const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  lintOnSave: false,

  pluginOptions: {
    quasar: {
      importStrategy: "kebab",
      rtlSupport: false,
    },
  },

  transpileDependencies: ["quasar"],
  devServer: {
    port: 5000, //端口號
    host: "localhost", //主機名
    https: false, //協議
    open: true, //啟動時是否自動打開瀏覽器
    // 開發環境代理配置
    proxy: {
      [process.env.VUE_APP_BASE_API]: {
        //代理別人
        target: process.env.VUE_APP_SERVICE_URL, //被代理
        ws: true, 

        changeOrigin: true, //啟動代理
        pathRewrite: {
          ["^" + process.env.VUE_APP_BASE_API]: "",
        },
      },
    },
  },
  lintOnSave: false, // 關閉格式檢查
  productionSourceMap: false, //打包時不會生成.map文件，加速打包
});
