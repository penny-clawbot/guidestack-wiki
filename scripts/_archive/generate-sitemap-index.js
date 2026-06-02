#!/usr/bin/env node
/**
 * generate-sitemap-index.js
 * Generates a master sitemap-index.xml referencing all 8 GuideStack site sitemaps.
 * Also regenerates individual site sitemaps with correct domain URLs.
 * 
 * Usage: node scripts/generate-sitemap-index.js [--output-dir ./output]
 * 
 * FREE — no paid tools required.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const configPath = path.join(rootDir, 'network-config.json');
const sitesDir = path.join(rootDir, 'output', 'sites');

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// --- Generate individual site sitemap.xml ---
function generateSiteSitemap(site) {
  const sitePath = path.join(sitesDir, site.id);
  const articlesDir = path.join(sitePath, 'src', 'content', 'articles');
  const distDir = path.join(sitePath, 'dist');
  
  if (!fs.existsSync(articlesDir)) {
    console.log(`  ⚠️  ${site.id}: No articles directory, skipping sitemap`);
    return null;
  }

  const siteUrl = `https://${site.domain}`;
  const urls = [];

  // Homepage
  urls.push({
    loc: siteUrl,
    changefreq: 'daily',
    priority: '1.0'
  });

  // Scan article markdown files
  const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.md'));
  for (const file of files) {
    const raw = fs.readFileSync(path.join(articlesDir, file), 'utf-8');
    
    // Extract slug from frontmatter or filename
    let slug = null;
    let lastmod = null;
    
    const slugMatch = raw.match(/^slug:\s*["']?(.+?)["']?\s*$/m);
    if (slugMatch) {
      slug = slugMatch[1];
    } else {
      // Derive from filename: strip date prefix and extension
      const nameMatch = file.match(/^\d{4}-\d{2}-\d{2}-(?:ai-)?(.+)\.md$/);
      if (nameMatch) {
        slug = nameMatch[1];
      } else {
        slug = file.replace(/\.md$/, '');
      }
    }

    // Skip utility pages
    if (['privacy-policy', 'terms', 'about', 'sitemap'].includes(slug)) continue;

    // Extract lastmod from frontmatter date or file stats
    const dateMatch = raw.match(/^date:\s*["']?(.+?)["']?\s*$/m) || file.match(/^(\d{4}-\d{2}-\d{2})/);
    if (dateMatch) lastmod = dateMatch[1];

    // Determine priority
    const isPillar = raw.includes('layout: pillar') || slug.includes('-guide-') || slug.includes('-complete-');
    const priority = isPillar ? '0.9' : '0.8';

    urls.push({
      loc: `${siteUrl}/${slug}`,
      lastmod: lastmod || undefined,
      changefreq: 'weekly',
      priority
    });
  }

  // Static pages
  for (const page of ['privacy-policy', 'about']) {
    if (files.some(f => f.includes(page))) {
      urls.push({
        loc: `${siteUrl}/${page}`,
        changefreq: 'monthly',
        priority: '0.3'
      });
    }
  }

  // Generate XML
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url><loc>${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}<changefreq>${u.changefreq}</changefreq><priority>${u.priority}</priority></url>`).join('\n')}
</urlset>`;

  // Write to dist/
  if (fs.existsSync(distDir)) {
    fs.writeFileSync(path.join(distDir, 'sitemap.xml'), xml);
    console.log(`  ✅ ${site.id}: ${urls.length} URLs written to dist/sitemap.xml`);
  }

  return { siteId: site.id, domain: site.domain, urlCount: urls.length };
}

// --- Generate master sitemap index ---
function generateSitemapIndex(results) {
  const validSites = results.filter(Boolean);
  const today = new Date().toISOString().split('T')[0];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${validSites.map(s => `  <sitemap>
    <loc>https://${s.domain}/sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>`).join('\n')}
</sitemapindex>`;

  // Write to network root
  const outputPath = path.join(rootDir, 'sitemap-index.xml');
  fs.writeFileSync(outputPath, xml);
  console.log(`\n📄 Master sitemap index written to: ${outputPath}`);
  console.log(`   ${validSites.length} sites referenced\n`);

  // Also write into each site's dist/ for self-hosting
  for (const site of config.sites) {
    const distDir = path.join(sitesDir, site.id, 'dist');
    if (fs.existsSync(distDir)) {
      fs.writeFileSync(path.join(distDir, 'sitemap-index.xml'), xml);
    }
  }
  console.log('  📋 sitemap-index.xml also copied to each site dist/');

  return xml;
}

// --- Main ---
console.log('🔍 PennyPress Network — Sitemap Generator\n');
console.log('Generating individual site sitemaps...');

const results = config.sites.map(site => generateSiteSitemap(site));
const indexXml = generateSitemapIndex(results);

// Print summary
console.log('\n📊 Summary:');
console.log('─'.repeat(50));
for (const r of results.filter(Boolean)) {
  console.log(`  ${r.domain}: ${r.urlCount} URLs`);
}
const totalUrls = results.filter(Boolean).reduce((sum, r) => sum + r.urlCount, 0);
console.log(`─`.repeat(50));
console.log(`  Total: ${totalUrls} URLs across ${results.filter(Boolean).length} sites`);
console.log('\n💡 Submit sitemap-index.xml to Google Search Console after deployment.');
