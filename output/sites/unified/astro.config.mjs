import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
export default defineConfig({ site: 'https://guidestack.wiki', integrations: [tailwind()], output: 'static', build: { inlineStylesheets: 'auto' }, vite: { build: { cssMinify: true } } });
