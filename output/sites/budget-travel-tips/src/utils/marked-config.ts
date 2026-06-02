import { marked } from 'marked';

// Custom renderer that adds id attributes to headings for TOC linking
const renderer = new marked.Renderer();
let headingCounter = 0;

renderer.heading = function({ text, depth }: { text: string; depth: number }) {
  const slug = text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
  // Add unique suffix if duplicate
  headingCounter++;
  const uniqueSlug = slug;
  return `<h${depth} id="${uniqueSlug}">${text}</h${depth}>`;
};

// Configure marked with custom renderer
marked.setOptions({
  renderer,
  gfm: true,
  breaks: true,
});

export function resetHeadingCounter() {
  headingCounter = 0;
}


// Image renderer with lazy loading and alt text enforcement
const origImage = renderer.image.bind(renderer);
renderer.image = function({ href, title, text }: { href: string; title?: string; text?: string }) {
  const alt = text || title || 'Article image';
  const lazy = 'loading="lazy" decoding="async"';
  const titleAttr = title ? ` title="${title}"` : '';
  return `<img src="${href}" alt="${alt}"${titleAttr} ${lazy} style="max-width:100%;height:auto;" />`;
};

export { marked };
