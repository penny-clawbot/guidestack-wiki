import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
export default defineConfig({ site: 'https://pennypress.com', integrations: [tailwind()], output: 'static', build: { inlineStylesheets: 'auto' }, vite: { build: { cssMinify: true } } });
