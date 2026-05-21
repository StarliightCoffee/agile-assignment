import { defineConfig } from 'vite'
import path from 'node:path'
import electron from 'vite-plugin-electron/simple'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isDesktopTarget = mode !== 'web'

  return {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    server: {
      proxy: {
        '/api/db-api/pay': { target: 'http://localhost:5427', changeOrigin: true },
        '/api/db-api': { target: 'http://localhost:5431', changeOrigin: true },
        '/api/account-mgmt': { target: 'http://localhost:5320', changeOrigin: true },
        '/api/': { target: 'http://localhost:5211', changeOrigin: true },
      },
    },
    plugins: [
      tailwindcss(),
      react(),
      ...(isDesktopTarget
        ? [
            electron({
              main: {
                // Shortcut of `build.lib.entry`.
                entry: 'electron/main.ts',
              },
              preload: {
                // Shortcut of `build.rollupOptions.input`.
                // Preload scripts may contain Web assets, so use the `build.rollupOptions.input` instead `build.lib.entry`.
                input: path.join(__dirname, 'electron/preload.ts'),
              },
              // Polyfill the Electron and Node.js API for Renderer process.
              // If you want use Node.js in Renderer process, `nodeIntegration` must be enabled in the Main process.
              // See https://github.com/electron-vite/vite-plugin-electron-renderer
              renderer:
                process.env.NODE_ENV === 'test'
                  // https://github.com/electron-vite/vite-plugin-electron-renderer/issues/78#issuecomment-2053600808
                  ? undefined
                  : {},
            }),
          ]
        : []),
    ],
  }
})
