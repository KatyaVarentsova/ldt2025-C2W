import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/C2W/',
  server: {
    proxy: {
      '/api': {
        target: 'http://89.169.177.178:8081',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
