import rss from '@astrojs/rss';
import fs from 'node:fs';
import path from 'node:path';

export function GET(context: any) {
  const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
  const domain = siteConfig.domain || 'example.com';
  const siteUrl = `https://${domain}`;

  const contentDir = 'src/content/articles';
  const articles: Array<{title: string; description: string; slug: string; date: string; category: string}> = [];

  if (fs.existsSync(contentDir)) {
    for (const file of fs.readdirSync(contentDir).filter(f => f.endsWith('.md'))) {
      const raw = fs.readFileSync(path.join(contentDir, file), 'utf-8');
      const fm: Record<string, string> = {};
      const fmMatch = raw.match(/^---\n([\s\S]*?)\n---/);
      if (fmMatch) {
        fmMatch[1].split('\n').forEach(line => {
          const m = line.match(/^(\w+):\s*["']?(.+?)["']?\s*$/);
          if (m) fm[m[1]] = m[2];
        });
      }
      articles.push({
        title: fm.title || file,
        description: fm.description || '',
        slug: file.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-(ai-)?/, ''),
        date: fm.date || new Date().toISOString().split('T')[0],
        category: fm.category || 'general',
      });
    }
  }

  articles.sort((a, b) => b.date.localeCompare(a.date));

  return rss({
    title: siteConfig.name,
    description: siteConfig.description,
    site: siteUrl,
    items: articles.slice(0, 50).map(article => ({
      title: article.title,
      pubDate: new Date(article.date + 'T00:00:00Z'),
      description: article.description,
      link: `${siteUrl}/${article.slug}`,
      categories: [article.category],
    })),
    customData: `<language>${siteConfig.language || 'en'}</language>`,
  });
}
