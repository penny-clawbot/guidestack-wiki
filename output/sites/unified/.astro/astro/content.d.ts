declare module 'astro:content' {
	interface RenderResult {
		Content: import('astro/runtime/server/index.js').AstroComponentFactory;
		headings: import('astro').MarkdownHeading[];
		remarkPluginFrontmatter: Record<string, any>;
	}
	interface Render {
		'.md': Promise<RenderResult>;
	}

	export interface RenderedContent {
		html: string;
		metadata?: {
			imagePaths: Array<string>;
			[key: string]: unknown;
		};
	}
}

declare module 'astro:content' {
	type Flatten<T> = T extends { [K: string]: infer U } ? U : never;

	export type CollectionKey = keyof AnyEntryMap;
	export type CollectionEntry<C extends CollectionKey> = Flatten<AnyEntryMap[C]>;

	export type ContentCollectionKey = keyof ContentEntryMap;
	export type DataCollectionKey = keyof DataEntryMap;

	type AllValuesOf<T> = T extends any ? T[keyof T] : never;
	type ValidContentEntrySlug<C extends keyof ContentEntryMap> = AllValuesOf<
		ContentEntryMap[C]
	>['slug'];

	/** @deprecated Use `getEntry` instead. */
	export function getEntryBySlug<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		// Note that this has to accept a regular string too, for SSR
		entrySlug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;

	/** @deprecated Use `getEntry` instead. */
	export function getDataEntryById<C extends keyof DataEntryMap, E extends keyof DataEntryMap[C]>(
		collection: C,
		entryId: E,
	): Promise<CollectionEntry<C>>;

	export function getCollection<C extends keyof AnyEntryMap, E extends CollectionEntry<C>>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => entry is E,
	): Promise<E[]>;
	export function getCollection<C extends keyof AnyEntryMap>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => unknown,
	): Promise<CollectionEntry<C>[]>;

	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(entry: {
		collection: C;
		slug: E;
	}): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(entry: {
		collection: C;
		id: E;
	}): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		slug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(
		collection: C,
		id: E,
	): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;

	/** Resolve an array of entry references from the same collection */
	export function getEntries<C extends keyof ContentEntryMap>(
		entries: {
			collection: C;
			slug: ValidContentEntrySlug<C>;
		}[],
	): Promise<CollectionEntry<C>[]>;
	export function getEntries<C extends keyof DataEntryMap>(
		entries: {
			collection: C;
			id: keyof DataEntryMap[C];
		}[],
	): Promise<CollectionEntry<C>[]>;

	export function render<C extends keyof AnyEntryMap>(
		entry: AnyEntryMap[C][string],
	): Promise<RenderResult>;

	export function reference<C extends keyof AnyEntryMap>(
		collection: C,
	): import('astro/zod').ZodEffects<
		import('astro/zod').ZodString,
		C extends keyof ContentEntryMap
			? {
					collection: C;
					slug: ValidContentEntrySlug<C>;
				}
			: {
					collection: C;
					id: keyof DataEntryMap[C];
				}
	>;
	// Allow generic `string` to avoid excessive type errors in the config
	// if `dev` is not running to update as you edit.
	// Invalid collection names will be caught at build time.
	export function reference<C extends string>(
		collection: C,
	): import('astro/zod').ZodEffects<import('astro/zod').ZodString, never>;

	type ReturnTypeOrOriginal<T> = T extends (...args: any[]) => infer R ? R : T;
	type InferEntrySchema<C extends keyof AnyEntryMap> = import('astro/zod').infer<
		ReturnTypeOrOriginal<Required<ContentConfig['collections'][C]>['schema']>
	>;

	type ContentEntryMap = {
		"articles": {
"ai-tools-about.md": {
	id: "ai-tools-about.md";
  slug: "ai-tools-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-coding-assistants-comparison.md": {
	id: "ai-tools-ai-coding-assistants-comparison.md";
  slug: "ai-tools-ai-coding-assistants-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-customer-service-tools.md": {
	id: "ai-tools-ai-customer-service-tools.md";
  slug: "ai-tools-ai-customer-service-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-ethics-and-safety-what-you-need-to-know.md": {
	id: "ai-tools-ai-ethics-and-safety-what-you-need-to-know.md";
  slug: "ai-tools-ai-ethics-and-safety-what-you-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-image-generators-midjourney-vs-dall-e-vs-stable-diffusion.md": {
	id: "ai-tools-ai-image-generators-midjourney-vs-dall-e-vs-stable-diffusion.md";
  slug: "ai-tools-ai-image-generators-midjourney-vs-dall-e-vs-stable-diffusion";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-meeting-note-taking-tools-comparison.md": {
	id: "ai-tools-ai-meeting-note-taking-tools-comparison.md";
  slug: "ai-tools-ai-meeting-note-taking-tools-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-productivity-hacks-10-ways-to-save-hours-every-week.md": {
	id: "ai-tools-ai-productivity-hacks-10-ways-to-save-hours-every-week.md";
  slug: "ai-tools-ai-productivity-hacks-10-ways-to-save-hours-every-week";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-productivity-tools-for-remote-workers.md": {
	id: "ai-tools-ai-productivity-tools-for-remote-workers.md";
  slug: "ai-tools-ai-productivity-tools-for-remote-workers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-ai-voice-and-video-tools-complete-overview.md": {
	id: "ai-tools-ai-voice-and-video-tools-complete-overview.md";
  slug: "ai-tools-ai-voice-and-video-tools-complete-overview";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-chatbots-compared.md": {
	id: "ai-tools-best-ai-chatbots-compared.md";
  slug: "ai-tools-best-ai-chatbots-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-coding-assistants-compared-copilot-vs-cursor-vs-windsurf.md": {
	id: "ai-tools-best-ai-coding-assistants-compared-copilot-vs-cursor-vs-windsurf.md";
  slug: "ai-tools-best-ai-coding-assistants-compared-copilot-vs-cursor-vs-windsurf";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-image-generators.md": {
	id: "ai-tools-best-ai-image-generators.md";
  slug: "ai-tools-best-ai-image-generators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-interior-design-tools.md": {
	id: "ai-tools-best-ai-interior-design-tools.md";
  slug: "ai-tools-best-ai-interior-design-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-music-generation-tools.md": {
	id: "ai-tools-best-ai-music-generation-tools.md";
  slug: "ai-tools-best-ai-music-generation-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-note-taking-apps.md": {
	id: "ai-tools-best-ai-note-taking-apps.md";
  slug: "ai-tools-best-ai-note-taking-apps";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-presentation-makers.md": {
	id: "ai-tools-best-ai-presentation-makers.md";
  slug: "ai-tools-best-ai-presentation-makers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-recipe-and-meal-planning-tools.md": {
	id: "ai-tools-best-ai-recipe-and-meal-planning-tools.md";
  slug: "ai-tools-best-ai-recipe-and-meal-planning-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-research-tools.md": {
	id: "ai-tools-best-ai-research-tools.md";
  slug: "ai-tools-best-ai-research-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-scheduling-assistants-2026.md": {
	id: "ai-tools-best-ai-scheduling-assistants-2026.md";
  slug: "ai-tools-best-ai-scheduling-assistants-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-scheduling-assistants.md": {
	id: "ai-tools-best-ai-scheduling-assistants.md";
  slug: "ai-tools-best-ai-scheduling-assistants";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-seo-tools-2026.md": {
	id: "ai-tools-best-ai-seo-tools-2026.md";
  slug: "ai-tools-best-ai-seo-tools-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-transcription-tools.md": {
	id: "ai-tools-best-ai-transcription-tools.md";
  slug: "ai-tools-best-ai-transcription-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-translation-tools.md": {
	id: "ai-tools-best-ai-translation-tools.md";
  slug: "ai-tools-best-ai-translation-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-video-editing-tools.md": {
	id: "ai-tools-best-ai-video-editing-tools.md";
  slug: "ai-tools-best-ai-video-editing-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-voice-over-tools.md": {
	id: "ai-tools-best-ai-voice-over-tools.md";
  slug: "ai-tools-best-ai-voice-over-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-writing-tools-2026.md": {
	id: "ai-tools-best-ai-writing-tools-2026.md";
  slug: "ai-tools-best-ai-writing-tools-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-ai-writing-tools-in-2026-compared.md": {
	id: "ai-tools-best-ai-writing-tools-in-2026-compared.md";
  slug: "ai-tools-best-ai-writing-tools-in-2026-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-accountants.md": {
	id: "ai-tools-best-for-accountants.md";
  slug: "ai-tools-best-for-accountants";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-affiliate-marketing.md": {
	id: "ai-tools-best-for-affiliate-marketing.md";
  slug: "ai-tools-best-for-affiliate-marketing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-brand-monitoring.md": {
	id: "ai-tools-best-for-brand-monitoring.md";
  slug: "ai-tools-best-for-brand-monitoring";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-cloud-infrastructure.md": {
	id: "ai-tools-best-for-cloud-infrastructure.md";
  slug: "ai-tools-best-for-cloud-infrastructure";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-content-creators.md": {
	id: "ai-tools-best-for-content-creators.md";
  slug: "ai-tools-best-for-content-creators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-customer-support.md": {
	id: "ai-tools-best-for-customer-support.md";
  slug: "ai-tools-best-for-customer-support";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-doctors.md": {
	id: "ai-tools-best-for-doctors.md";
  slug: "ai-tools-best-for-doctors";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-email-automation.md": {
	id: "ai-tools-best-for-email-automation.md";
  slug: "ai-tools-best-for-email-automation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-forex-trading.md": {
	id: "ai-tools-best-for-forex-trading.md";
  slug: "ai-tools-best-for-forex-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-fraud-detection.md": {
	id: "ai-tools-best-for-fraud-detection.md";
  slug: "ai-tools-best-for-fraud-detection";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-game-development.md": {
	id: "ai-tools-best-for-game-development.md";
  slug: "ai-tools-best-for-game-development";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-machine-learning.md": {
	id: "ai-tools-best-for-machine-learning.md";
  slug: "ai-tools-best-for-machine-learning";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-market-research.md": {
	id: "ai-tools-best-for-market-research.md";
  slug: "ai-tools-best-for-market-research";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-marketers.md": {
	id: "ai-tools-best-for-marketers.md";
  slug: "ai-tools-best-for-marketers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-natural-language-processing.md": {
	id: "ai-tools-best-for-natural-language-processing.md";
  slug: "ai-tools-best-for-natural-language-processing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-qa-testing.md": {
	id: "ai-tools-best-for-qa-testing.md";
  slug: "ai-tools-best-for-qa-testing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-sales-forecasting.md": {
	id: "ai-tools-best-for-sales-forecasting.md";
  slug: "ai-tools-best-for-sales-forecasting";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-stock-market-analysis.md": {
	id: "ai-tools-best-for-stock-market-analysis.md";
  slug: "ai-tools-best-for-stock-market-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-supply-chain-management.md": {
	id: "ai-tools-best-for-supply-chain-management.md";
  slug: "ai-tools-best-for-supply-chain-management";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-teachers.md": {
	id: "ai-tools-best-for-teachers.md";
  slug: "ai-tools-best-for-teachers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-ux-design.md": {
	id: "ai-tools-best-for-ux-design.md";
  slug: "ai-tools-best-for-ux-design";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-for-video-production.md": {
	id: "ai-tools-best-for-video-production.md";
  slug: "ai-tools-best-for-video-production";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-best-free-for-students-and-professionals.md": {
	id: "ai-tools-best-free-for-students-and-professionals.md";
  slug: "ai-tools-best-free-for-students-and-professionals";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-credit-card-points-for-travel-complete-beginner-guide.md": {
	id: "ai-tools-credit-card-points-for-travel-complete-beginner-guide.md";
  slug: "ai-tools-credit-card-points-for-travel-complete-beginner-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-faq-everything-beginners-need-to-know.md": {
	id: "ai-tools-faq-everything-beginners-need-to-know.md";
  slug: "ai-tools-faq-everything-beginners-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-animation.md": {
	id: "ai-tools-for-animation.md";
  slug: "ai-tools-for-animation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-app-development.md": {
	id: "ai-tools-for-app-development.md";
  slug: "ai-tools-for-app-development";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-business-intelligence.md": {
	id: "ai-tools-for-business-intelligence.md";
  slug: "ai-tools-for-business-intelligence";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-competitive-analysis.md": {
	id: "ai-tools-for-competitive-analysis.md";
  slug: "ai-tools-for-competitive-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-crypto-traders.md": {
	id: "ai-tools-for-crypto-traders.md";
  slug: "ai-tools-for-crypto-traders";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-customer-retention.md": {
	id: "ai-tools-for-customer-retention.md";
  slug: "ai-tools-for-customer-retention";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-cybersecurity.md": {
	id: "ai-tools-for-cybersecurity.md";
  slug: "ai-tools-for-cybersecurity";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-data-analysis.md": {
	id: "ai-tools-for-data-analysis.md";
  slug: "ai-tools-for-data-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-data-engineering.md": {
	id: "ai-tools-for-data-engineering.md";
  slug: "ai-tools-for-data-engineering";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-deep-learning.md": {
	id: "ai-tools-for-deep-learning.md";
  slug: "ai-tools-for-deep-learning";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-devops-automation.md": {
	id: "ai-tools-for-devops-automation.md";
  slug: "ai-tools-for-devops-automation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-dropshippers.md": {
	id: "ai-tools-for-dropshippers.md";
  slug: "ai-tools-for-dropshippers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-ecommerce-stores.md": {
	id: "ai-tools-for-ecommerce-stores.md";
  slug: "ai-tools-for-ecommerce-stores";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-email-marketing.md": {
	id: "ai-tools-for-email-marketing.md";
  slug: "ai-tools-for-email-marketing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-financial-planning.md": {
	id: "ai-tools-for-financial-planning.md";
  slug: "ai-tools-for-financial-planning";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-fitness-and-health-tracking.md": {
	id: "ai-tools-for-fitness-and-health-tracking.md";
  slug: "ai-tools-for-fitness-and-health-tracking";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-graphic-design.md": {
	id: "ai-tools-for-graphic-design.md";
  slug: "ai-tools-for-graphic-design";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-hr-and-recruiting.md": {
	id: "ai-tools-for-hr-and-recruiting.md";
  slug: "ai-tools-for-hr-and-recruiting";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-influencer-marketing.md": {
	id: "ai-tools-for-influencer-marketing.md";
  slug: "ai-tools-for-influencer-marketing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-inventory-tracking.md": {
	id: "ai-tools-for-inventory-tracking.md";
  slug: "ai-tools-for-inventory-tracking";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-lawyers.md": {
	id: "ai-tools-for-lawyers.md";
  slug: "ai-tools-for-lawyers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-lead-generation.md": {
	id: "ai-tools-for-lead-generation.md";
  slug: "ai-tools-for-lead-generation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-legal-professionals.md": {
	id: "ai-tools-for-legal-professionals.md";
  slug: "ai-tools-for-legal-professionals";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-mental-health-support.md": {
	id: "ai-tools-for-mental-health-support.md";
  slug: "ai-tools-for-mental-health-support";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-personal-shoppers.md": {
	id: "ai-tools-for-personal-shoppers.md";
  slug: "ai-tools-for-personal-shoppers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-podcast-creators.md": {
	id: "ai-tools-for-podcast-creators.md";
  slug: "ai-tools-for-podcast-creators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-product-development.md": {
	id: "ai-tools-for-product-development.md";
  slug: "ai-tools-for-product-development";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-project-management.md": {
	id: "ai-tools-for-project-management.md";
  slug: "ai-tools-for-project-management";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-real-estate-agents.md": {
	id: "ai-tools-for-real-estate-agents.md";
  slug: "ai-tools-for-real-estate-agents";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-small-business-owners.md": {
	id: "ai-tools-for-small-business-owners.md";
  slug: "ai-tools-for-small-business-owners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-social-media-management.md": {
	id: "ai-tools-for-social-media-management.md";
  slug: "ai-tools-for-social-media-management";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-for-website-building.md": {
	id: "ai-tools-for-website-building.md";
  slug: "ai-tools-for-website-building";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-free-ai-alternatives-to-paid-tools.md": {
	id: "ai-tools-free-ai-alternatives-to-paid-tools.md";
  slug: "ai-tools-free-ai-alternatives-to-paid-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-free-for-designers.md": {
	id: "ai-tools-free-for-designers.md";
  slug: "ai-tools-free-for-designers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-free-for-nonprofits.md": {
	id: "ai-tools-free-for-nonprofits.md";
  slug: "ai-tools-free-for-nonprofits";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-free-for-startups.md": {
	id: "ai-tools-free-for-startups.md";
  slug: "ai-tools-free-for-startups";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-ai-is-changing-digital-marketing-in-2026.md": {
	id: "ai-tools-how-ai-is-changing-digital-marketing-in-2026.md";
  slug: "ai-tools-how-ai-is-changing-digital-marketing-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-to-automate-your-business-with-ai.md": {
	id: "ai-tools-how-to-automate-your-business-with-ai.md";
  slug: "ai-tools-how-to-automate-your-business-with-ai";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-to-build-an-ai-powered-business-in-2026.md": {
	id: "ai-tools-how-to-build-an-ai-powered-business-in-2026.md";
  slug: "ai-tools-how-to-build-an-ai-powered-business-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-to-create-ai-art-beginner-to-advanced-guide.md": {
	id: "ai-tools-how-to-create-ai-art-beginner-to-advanced-guide.md";
  slug: "ai-tools-how-to-create-ai-art-beginner-to-advanced-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-to-travel-southeast-asia-on-0-a-day.md": {
	id: "ai-tools-how-to-travel-southeast-asia-on-0-a-day.md";
  slug: "ai-tools-how-to-travel-southeast-asia-on-0-a-day";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-how-to-use-chatgpt-effectively-complete-guide.md": {
	id: "ai-tools-how-to-use-chatgpt-effectively-complete-guide.md";
  slug: "ai-tools-how-to-use-chatgpt-effectively-complete-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-privacy-policy.md": {
	id: "ai-tools-privacy-policy.md";
  slug: "ai-tools-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-terms-of-service.md": {
	id: "ai-tools-terms-of-service.md";
  slug: "ai-tools-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"ai-tools-top-15-that-will-transform-your-workflow.md": {
	id: "ai-tools-top-15-that-will-transform-your-workflow.md";
  slug: "ai-tools-top-15-that-will-transform-your-workflow";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-about.md": {
	id: "bitcoin-beginners-about.md";
  slug: "bitcoin-beginners-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-best-bitcoin-apps-for-beginners.md": {
	id: "bitcoin-beginners-best-bitcoin-apps-for-beginners.md";
  slug: "bitcoin-beginners-best-bitcoin-apps-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-best-bitcoin-basics-beginner-guide-strategies-for-2026.md": {
	id: "bitcoin-beginners-best-bitcoin-basics-beginner-guide-strategies-for-2026.md";
  slug: "bitcoin-beginners-best-bitcoin-basics-beginner-guide-strategies-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-best-bitcoin-podcasts-to-follow.md": {
	id: "bitcoin-beginners-best-bitcoin-podcasts-to-follow.md";
  slug: "bitcoin-beginners-best-bitcoin-podcasts-to-follow";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-and-environmental-impact.md": {
	id: "bitcoin-beginners-bitcoin-and-environmental-impact.md";
  slug: "bitcoin-beginners-bitcoin-and-environmental-impact";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-and-taxes-what-you-need-to-know.md": {
	id: "bitcoin-beginners-bitcoin-and-taxes-what-you-need-to-know.md";
  slug: "bitcoin-beginners-bitcoin-and-taxes-what-you-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-atm-how-to-use.md": {
	id: "bitcoin-beginners-bitcoin-atm-how-to-use.md";
  slug: "bitcoin-beginners-bitcoin-atm-how-to-use";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-atms-near-me-how-to-buy-bitcoin-with-cash-in-2026.md": {
	id: "bitcoin-beginners-bitcoin-atms-near-me-how-to-buy-bitcoin-with-cash-in-2026.md";
  slug: "bitcoin-atms-near-me-how-to-buy-bitcoin-with-cash-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-brain-wallet-risks.md": {
	id: "bitcoin-beginners-bitcoin-brain-wallet-risks.md";
  slug: "bitcoin-beginners-bitcoin-brain-wallet-risks";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-child-pays-for-parent-cpfp.md": {
	id: "bitcoin-beginners-bitcoin-child-pays-for-parent-cpfp.md";
  slug: "bitcoin-beginners-bitcoin-child-pays-for-parent-cpfp";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-coin-control-features.md": {
	id: "bitcoin-beginners-bitcoin-coin-control-features.md";
  slug: "bitcoin-beginners-bitcoin-coin-control-features";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-cold-storage-best-practices.md": {
	id: "bitcoin-beginners-bitcoin-cold-storage-best-practices.md";
  slug: "bitcoin-beginners-bitcoin-cold-storage-best-practices";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-debit-cards-compared.md": {
	id: "bitcoin-beginners-bitcoin-debit-cards-compared.md";
  slug: "bitcoin-beginners-bitcoin-debit-cards-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-defi-explained-how-decentralized-finance-works-with-bitcoin.md": {
	id: "bitcoin-beginners-bitcoin-defi-explained-how-decentralized-finance-works-with-bitcoin.md";
  slug: "bitcoin-defi-explained-how-decentralized-finance-works-with-bitcoin";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-etf-vs-direct-ownership-pros-cons.md": {
	id: "bitcoin-beginners-bitcoin-etf-vs-direct-ownership-pros-cons.md";
  slug: "bitcoin-beginners-bitcoin-etf-vs-direct-ownership-pros-cons";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-etfs-guide.md": {
	id: "bitcoin-beginners-bitcoin-etfs-guide.md";
  slug: "bitcoin-etfs-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-fee-estimation-guide.md": {
	id: "bitcoin-beginners-bitcoin-fee-estimation-guide.md";
  slug: "bitcoin-beginners-bitcoin-fee-estimation-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-for-small-business-owners.md": {
	id: "bitcoin-beginners-bitcoin-for-small-business-owners.md";
  slug: "bitcoin-beginners-bitcoin-for-small-business-owners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-forks-explained-simply.md": {
	id: "bitcoin-beginners-bitcoin-forks-explained-simply.md";
  slug: "bitcoin-beginners-bitcoin-forks-explained-simply";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-forks-hard-forks-vs-soft-forks-explained.md": {
	id: "bitcoin-beginners-bitcoin-forks-hard-forks-vs-soft-forks-explained.md";
  slug: "bitcoin-forks-hard-forks-vs-soft-forks-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-history-and-timeline.md": {
	id: "bitcoin-beginners-bitcoin-history-and-timeline.md";
  slug: "bitcoin-beginners-bitcoin-history-and-timeline";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-key-generation-methods.md": {
	id: "bitcoin-beginners-bitcoin-key-generation-methods.md";
  slug: "bitcoin-beginners-bitcoin-key-generation-methods";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-lightning-network-channels.md": {
	id: "bitcoin-beginners-bitcoin-lightning-network-channels.md";
  slug: "bitcoin-beginners-bitcoin-lightning-network-channels";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-mixers-and-privacy.md": {
	id: "bitcoin-beginners-bitcoin-mixers-and-privacy.md";
  slug: "bitcoin-beginners-bitcoin-mixers-and-privacy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-multisig-wallets-guide.md": {
	id: "bitcoin-beginners-bitcoin-multisig-wallets-guide.md";
  slug: "bitcoin-beginners-bitcoin-multisig-wallets-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-node-setup-guide-beginners.md": {
	id: "bitcoin-beginners-bitcoin-node-setup-guide-beginners.md";
  slug: "bitcoin-beginners-bitcoin-node-setup-guide-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-paper-wallet-guide.md": {
	id: "bitcoin-beginners-bitcoin-paper-wallet-guide.md";
  slug: "bitcoin-beginners-bitcoin-paper-wallet-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-price-history-from-pennies-to-thousands.md": {
	id: "bitcoin-beginners-bitcoin-price-history-from-pennies-to-thousands.md";
  slug: "bitcoin-price-history-from-pennies-to-thousands";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-price-prediction-2026.md": {
	id: "bitcoin-beginners-bitcoin-price-prediction-2026.md";
  slug: "bitcoin-beginners-bitcoin-price-prediction-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-private-keys-explained.md": {
	id: "bitcoin-beginners-bitcoin-private-keys-explained.md";
  slug: "bitcoin-beginners-bitcoin-private-keys-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-raw-transaction-guide.md": {
	id: "bitcoin-beginners-bitcoin-raw-transaction-guide.md";
  slug: "bitcoin-beginners-bitcoin-raw-transaction-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-refund-policies-explained.md": {
	id: "bitcoin-beginners-bitcoin-refund-policies-explained.md";
  slug: "bitcoin-beginners-bitcoin-refund-policies-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-regulations-by-country.md": {
	id: "bitcoin-beginners-bitcoin-regulations-by-country.md";
  slug: "bitcoin-beginners-bitcoin-regulations-by-country";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-replace-by-fee-rbf.md": {
	id: "bitcoin-beginners-bitcoin-replace-by-fee-rbf.md";
  slug: "bitcoin-beginners-bitcoin-replace-by-fee-rbf";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-scalability-solutions.md": {
	id: "bitcoin-beginners-bitcoin-scalability-solutions.md";
  slug: "bitcoin-beginners-bitcoin-scalability-solutions";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-security-best-practices.md": {
	id: "bitcoin-beginners-bitcoin-security-best-practices.md";
  slug: "bitcoin-beginners-bitcoin-security-best-practices";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-sign-message-verify.md": {
	id: "bitcoin-beginners-bitcoin-sign-message-verify.md";
  slug: "bitcoin-beginners-bitcoin-sign-message-verify";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-soft-fork-vs-hard-fork.md": {
	id: "bitcoin-beginners-bitcoin-soft-fork-vs-hard-fork.md";
  slug: "bitcoin-beginners-bitcoin-soft-fork-vs-hard-fork";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-tax-guide-what-you-need-to-know.md": {
	id: "bitcoin-beginners-bitcoin-tax-guide-what-you-need-to-know.md";
  slug: "bitcoin-tax-guide-what-you-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-transaction-fees-explained.md": {
	id: "bitcoin-beginners-bitcoin-transaction-fees-explained.md";
  slug: "bitcoin-beginners-bitcoin-transaction-fees-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-vs-ethereum-differences.md": {
	id: "bitcoin-beginners-bitcoin-vs-ethereum-differences.md";
  slug: "bitcoin-beginners-bitcoin-vs-ethereum-differences";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-vs-ethereum-key-differences-explained.md": {
	id: "bitcoin-beginners-bitcoin-vs-ethereum-key-differences-explained.md";
  slug: "bitcoin-vs-ethereum-key-differences-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-vs-gold-comparison.md": {
	id: "bitcoin-beginners-bitcoin-vs-gold-comparison.md";
  slug: "bitcoin-beginners-bitcoin-vs-gold-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-vs-traditional-money.md": {
	id: "bitcoin-beginners-bitcoin-vs-traditional-money.md";
  slug: "bitcoin-beginners-bitcoin-vs-traditional-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-wallet-types-explained.md": {
	id: "bitcoin-beginners-bitcoin-wallet-types-explained.md";
  slug: "bitcoin-beginners-bitcoin-wallet-types-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-wallets-explained-hardware-software-and-paper-wallets.md": {
	id: "bitcoin-beginners-bitcoin-wallets-explained-hardware-software-and-paper-wallets.md";
  slug: "bitcoin-wallets-explained-hardware-software-and-paper-wallets";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-bitcoin-witness-segwit-explained.md": {
	id: "bitcoin-beginners-bitcoin-witness-segwit-explained.md";
  slug: "bitcoin-beginners-bitcoin-witness-segwit-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-budget-travel-packing-list-the-ultimate-guide.md": {
	id: "bitcoin-beginners-budget-travel-packing-list-the-ultimate-guide.md";
  slug: "bitcoin-beginners-budget-travel-packing-list-the-ultimate-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-central-bank-digital-currencies-vs-bitcoin.md": {
	id: "bitcoin-beginners-central-bank-digital-currencies-vs-bitcoin.md";
  slug: "bitcoin-beginners-central-bank-digital-currencies-vs-bitcoin";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-bitcoin-mining-works.md": {
	id: "bitcoin-beginners-how-bitcoin-mining-works.md";
  slug: "bitcoin-beginners-how-bitcoin-mining-works";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-accept-bitcoin-payments-as-a-business.md": {
	id: "bitcoin-beginners-how-to-accept-bitcoin-payments-as-a-business.md";
  slug: "how-to-accept-bitcoin-payments-as-a-business-a-complete-guide-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-accept-bitcoin-payments.md": {
	id: "bitcoin-beginners-how-to-accept-bitcoin-payments.md";
  slug: "bitcoin-beginners-how-to-accept-bitcoin-payments";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-avoid-bitcoin-scams-and-fraud.md": {
	id: "bitcoin-beginners-how-to-avoid-bitcoin-scams-and-fraud.md";
  slug: "how-to-avoid-bitcoin-scams-and-fraud";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-buy-bitcoin-for-beginners.md": {
	id: "bitcoin-beginners-how-to-buy-bitcoin-for-beginners.md";
  slug: "bitcoin-beginners-how-to-buy-bitcoin-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-buy-bitcoin-for-the-first-time.md": {
	id: "bitcoin-beginners-how-to-buy-bitcoin-for-the-first-time.md";
  slug: "how-to-buy-bitcoin-for-the-first-time";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-create-a-bitcoin-wallet.md": {
	id: "bitcoin-beginners-how-to-create-a-bitcoin-wallet.md";
  slug: "bitcoin-beginners-how-to-create-a-bitcoin-wallet";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-earn-bitcoin-without-buying.md": {
	id: "bitcoin-beginners-how-to-earn-bitcoin-without-buying.md";
  slug: "bitcoin-beginners-how-to-earn-bitcoin-without-buying";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-keep-your-bitcoin-safe-and-secure.md": {
	id: "bitcoin-beginners-how-to-keep-your-bitcoin-safe-and-secure.md";
  slug: "";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-read-bitcoin-charts.md": {
	id: "bitcoin-beginners-how-to-read-bitcoin-charts.md";
  slug: "bitcoin-beginners-how-to-read-bitcoin-charts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-send-and-receive-bitcoin.md": {
	id: "bitcoin-beginners-how-to-send-and-receive-bitcoin.md";
  slug: "bitcoin-beginners-how-to-send-and-receive-bitcoin";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-store-bitcoin-safely.md": {
	id: "bitcoin-beginners-how-to-store-bitcoin-safely.md";
  slug: "bitcoin-beginners-how-to-store-bitcoin-safely";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-how-to-travel-southeast-asia-on-0-a-day.md": {
	id: "bitcoin-beginners-how-to-travel-southeast-asia-on-0-a-day.md";
  slug: "bitcoin-beginners-how-to-travel-southeast-asia-on-0-a-day";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-is-bitcoin-a-good-investment-2026.md": {
	id: "bitcoin-beginners-is-bitcoin-a-good-investment-2026.md";
  slug: "bitcoin-beginners-is-bitcoin-a-good-investment-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-lightning-network-explained-simply.md": {
	id: "bitcoin-beginners-lightning-network-explained-simply.md";
  slug: "bitcoin-beginners-lightning-network-explained-simply";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-privacy-policy.md": {
	id: "bitcoin-beginners-privacy-policy.md";
  slug: "bitcoin-beginners-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-terms-of-service.md": {
	id: "bitcoin-beginners-terms-of-service.md";
  slug: "bitcoin-beginners-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-the-environmental-impact-of-bitcoin-mining.md": {
	id: "bitcoin-beginners-the-environmental-impact-of-bitcoin-mining.md";
  slug: "the-environmental-impact-of-bitcoin-mining-what-every-investor-needs-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-understanding-bitcoin-addresses.md": {
	id: "bitcoin-beginners-understanding-bitcoin-addresses.md";
  slug: "bitcoin-beginners-understanding-bitcoin-addresses";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-understanding-bitcoin-halving-cycles.md": {
	id: "bitcoin-beginners-understanding-bitcoin-halving-cycles.md";
  slug: "understanding-bitcoin-halving-cycles";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-understanding-bitcoin-halving.md": {
	id: "bitcoin-beginners-understanding-bitcoin-halving.md";
  slug: "bitcoin-beginners-understanding-bitcoin-halving";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-what-is-a-bitcoin-hardware-wallet.md": {
	id: "bitcoin-beginners-what-is-a-bitcoin-hardware-wallet.md";
  slug: "bitcoin-beginners-what-is-a-bitcoin-hardware-wallet";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-what-is-bitcoin-a-complete-beginners-guide.md": {
	id: "bitcoin-beginners-what-is-bitcoin-a-complete-beginners-guide.md";
  slug: "what-is-bitcoin-a-complete-beginners-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-what-is-bitcoin-explained-simply.md": {
	id: "bitcoin-beginners-what-is-bitcoin-explained-simply.md";
  slug: "bitcoin-beginners-what-is-bitcoin-explained-simply";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-what-is-bitcoin-mining-and-how-does-it-work.md": {
	id: "bitcoin-beginners-what-is-bitcoin-mining-and-how-does-it-work.md";
  slug: "what-is-bitcoin-mining-and-how-does-it-work-a-complete-beginners-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"bitcoin-beginners-what-is-the-bitcoin-lightning-network.md": {
	id: "bitcoin-beginners-what-is-the-bitcoin-lightning-network.md";
  slug: "what-is-the-bitcoin-lightning-network";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-about.md": {
	id: "budget-travel-about.md";
  slug: "budget-travel-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-affordable-adventure-travel-activities.md": {
	id: "budget-travel-affordable-adventure-travel-activities.md";
  slug: "budget-travel-affordable-adventure-travel-activities";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-affordable-beach-destinations-caribbean.md": {
	id: "budget-travel-affordable-beach-destinations-caribbean.md";
  slug: "budget-travel-affordable-beach-destinations-caribbean";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-affordable-honeymoon-destinations-under-3000.md": {
	id: "budget-travel-affordable-honeymoon-destinations-under-3000.md";
  slug: "budget-travel-affordable-honeymoon-destinations-under-3000";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-affordable-road-trip-routes-in-usa.md": {
	id: "budget-travel-affordable-road-trip-routes-in-usa.md";
  slug: "budget-travel-affordable-road-trip-routes-in-usa";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-apps-2026.md": {
	id: "budget-travel-best-apps-2026.md";
  slug: "budget-travel-best-apps-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-apps-for-2026.md": {
	id: "budget-travel-best-apps-for-2026.md";
  slug: "budget-travel-best-apps-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-apps-for-budget-travelers.md": {
	id: "budget-travel-best-apps-for-budget-travelers.md";
  slug: "budget-travel-best-apps-for-budget-travelers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-budget-airlines-for-international-travel.md": {
	id: "budget-travel-best-budget-airlines-for-international-travel.md";
  slug: "budget-travel-best-budget-airlines-for-international-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-budget-hostels-in-europe.md": {
	id: "budget-travel-best-budget-hostels-in-europe.md";
  slug: "budget-travel-best-budget-hostels-in-europe";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-destinations-for-families.md": {
	id: "budget-travel-best-destinations-for-families.md";
  slug: "budget-travel-best-destinations-for-families";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-european-cities-for-budget-travelers-under-30.md": {
	id: "budget-travel-best-european-cities-for-budget-travelers-under-30.md";
  slug: "budget-travel-best-european-cities-for-budget-travelers-under-30";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-gear-essentials.md": {
	id: "budget-travel-best-gear-essentials.md";
  slug: "budget-travel-best-gear-essentials";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-gear-under-50.md": {
	id: "budget-travel-best-gear-under-50.md";
  slug: "budget-travel-best-gear-under-50";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-insurance-options-compared.md": {
	id: "budget-travel-best-insurance-options-compared.md";
  slug: "budget-travel-best-insurance-options-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-options-compared.md": {
	id: "budget-travel-best-options-compared.md";
  slug: "budget-travel-best-options-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-strategies-for-2026.md": {
	id: "budget-travel-best-strategies-for-2026.md";
  slug: "budget-travel-best-strategies-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-tips-2024.md": {
	id: "budget-travel-best-tips-2024.md";
  slug: "budget-travel-best-tips-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-tips-amazon.md": {
	id: "budget-travel-best-tips-amazon.md";
  slug: "budget-travel-best-tips-amazon";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-tips-for-2026.md": {
	id: "budget-travel-best-tips-for-2026.md";
  slug: "budget-travel-best-tips-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-tips-for-beginners.md": {
	id: "budget-travel-best-tips-for-beginners.md";
  slug: "budget-travel-best-tips-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-tips-forum.md": {
	id: "budget-travel-best-tips-forum.md";
  slug: "budget-travel-best-tips-forum";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-travel-hacks-for-saving-money-2026.md": {
	id: "budget-travel-best-travel-hacks-for-saving-money-2026.md";
  slug: "budget-travel-best-travel-hacks-for-saving-money-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-best-travel-rewards-credit-cards-for-beginners.md": {
	id: "budget-travel-best-travel-rewards-credit-cards-for-beginners.md";
  slug: "budget-travel-best-travel-rewards-credit-cards-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-budget-friendly-national-parks-to-visit.md": {
	id: "budget-travel-budget-friendly-national-parks-to-visit.md";
  slug: "budget-travel-budget-friendly-national-parks-to-visit";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-budget-safari-tours-in-africa.md": {
	id: "budget-travel-budget-safari-tours-in-africa.md";
  slug: "budget-travel-budget-safari-tours-in-africa";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-cheap-flights-hacks-that-actually-work-in-2026.md": {
	id: "budget-travel-cheap-flights-hacks-that-actually-work-in-2026.md";
  slug: "budget-travel-cheap-flights-hacks-that-actually-work-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-cheapest-cities-to-live-in-europe-2026.md": {
	id: "budget-travel-cheapest-cities-to-live-in-europe-2026.md";
  slug: "budget-travel-cheapest-cities-to-live-in-europe-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-cheapest-countries-to-visit-in-2026.md": {
	id: "budget-travel-cheapest-countries-to-visit-in-2026.md";
  slug: "budget-travel-cheapest-countries-to-visit-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-cheapest-time-to-fly-to-europe.md": {
	id: "budget-travel-cheapest-time-to-fly-to-europe.md";
  slug: "budget-travel-cheapest-time-to-fly-to-europe";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-cheapest-ways-to-travel-between-cities.md": {
	id: "budget-travel-cheapest-ways-to-travel-between-cities.md";
  slug: "budget-travel-cheapest-ways-to-travel-between-cities";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-complete-guide-for-2026.md": {
	id: "budget-travel-complete-guide-for-2026.md";
  slug: "budget-travel-complete-guide-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-faq-20-common-questions-answered.md": {
	id: "budget-travel-faq-20-common-questions-answered.md";
  slug: "budget-travel-faq-20-common-questions-answered";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-faq-common-questions-answered.md": {
	id: "budget-travel-faq-common-questions-answered.md";
  slug: "budget-travel-faq-common-questions-answered";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-for-digital-nomads.md": {
	id: "budget-travel-for-digital-nomads.md";
  slug: "budget-travel-for-digital-nomads";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-free-vs-paid-which-is-better.md": {
	id: "budget-travel-free-vs-paid-which-is-better.md";
  slug: "budget-travel-free-vs-paid-which-is-better";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-hacks-that-save-time.md": {
	id: "budget-travel-hacks-that-save-time.md";
  slug: "budget-travel-hacks-that-save-time";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-choose-the-right-strategy.md": {
	id: "budget-travel-how-to-choose-the-right-strategy.md";
  slug: "budget-travel-how-to-choose-the-right-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-find-budget-accommodation-anywhere.md": {
	id: "budget-travel-how-to-find-budget-accommodation-anywhere.md";
  slug: "budget-travel-how-to-find-budget-accommodation-anywhere";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-find-cheap-accommodation-anywhere.md": {
	id: "budget-travel-how-to-find-cheap-accommodation-anywhere.md";
  slug: "budget-travel-how-to-find-cheap-accommodation-anywhere";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-find-cheap-flights-last-minute.md": {
	id: "budget-travel-how-to-find-cheap-flights-last-minute.md";
  slug: "budget-travel-how-to-find-cheap-flights-last-minute";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-find-hidden-gem-destinations.md": {
	id: "budget-travel-how-to-find-hidden-gem-destinations.md";
  slug: "budget-travel-how-to-find-hidden-gem-destinations";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-get-cheap-hotel-upgrades.md": {
	id: "budget-travel-how-to-get-cheap-hotel-upgrades.md";
  slug: "budget-travel-how-to-get-cheap-hotel-upgrades";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-get-started-with-budget-travel.md": {
	id: "budget-travel-how-to-get-started-with-budget-travel.md";
  slug: "budget-travel-how-to-get-started-with-budget-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-plan-a-budget-trip-step-by-step.md": {
	id: "budget-travel-how-to-plan-a-budget-trip-step-by-step.md";
  slug: "budget-travel-how-to-plan-a-budget-trip-step-by-step";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-plan-a-budget-trip-to-mexico.md": {
	id: "budget-travel-how-to-plan-a-budget-trip-to-mexico.md";
  slug: "budget-travel-how-to-plan-a-budget-trip-to-mexico";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-save-money-on-food-while-traveling.md": {
	id: "budget-travel-how-to-save-money-on-food-while-traveling.md";
  slug: "budget-travel-how-to-save-money-on-food-while-traveling";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-during-peak-season-without-breaking-the-bank.md": {
	id: "budget-travel-how-to-travel-during-peak-season-without-breaking-the-bank.md";
  slug: "budget-travel-how-to-travel-during-peak-season-without-breaking-the-bank";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-europe-on-50-a-day.md": {
	id: "budget-travel-how-to-travel-europe-on-50-a-day.md";
  slug: "budget-travel-how-to-travel-europe-on-50-a-day";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-full-time-on-a-budget.md": {
	id: "budget-travel-how-to-travel-full-time-on-a-budget.md";
  slug: "budget-travel-how-to-travel-full-time-on-a-budget";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-japan-on-a-budget.md": {
	id: "budget-travel-how-to-travel-japan-on-a-budget.md";
  slug: "budget-travel-how-to-travel-japan-on-a-budget";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-southeast-asia-on-30-a-day.md": {
	id: "budget-travel-how-to-travel-southeast-asia-on-30-a-day.md";
  slug: "budget-travel-how-to-travel-southeast-asia-on-30-a-day";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-travel-with-only-a-carry-on.md": {
	id: "budget-travel-how-to-travel-with-only-a-carry-on.md";
  slug: "budget-travel-how-to-travel-with-only-a-carry-on";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-use-airline-miles-effectively.md": {
	id: "budget-travel-how-to-use-airline-miles-effectively.md";
  slug: "budget-travel-how-to-use-airline-miles-effectively";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-use-credit-card-points-for-free-flights.md": {
	id: "budget-travel-how-to-use-credit-card-points-for-free-flights.md";
  slug: "budget-travel-how-to-use-credit-card-points-for-free-flights";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-how-to-use-points-and-miles-for-free-travel.md": {
	id: "budget-travel-how-to-use-points-and-miles-for-free-travel.md";
  slug: "budget-travel-how-to-use-points-and-miles-for-free-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-insurance-worth-it.md": {
	id: "budget-travel-insurance-worth-it.md";
  slug: "budget-travel-insurance-worth-it";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-mistakes-that-cost-you-money.md": {
	id: "budget-travel-mistakes-that-cost-you-money.md";
  slug: "budget-travel-mistakes-that-cost-you-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-mistakes-that-could-ruin-your-trip.md": {
	id: "budget-travel-mistakes-that-could-ruin-your-trip.md";
  slug: "budget-travel-mistakes-that-could-ruin-your-trip";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-mistakes-to-avoid.md": {
	id: "budget-travel-mistakes-to-avoid.md";
  slug: "budget-travel-mistakes-to-avoid";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-off-season-travel-deals-and-tips.md": {
	id: "budget-travel-off-season-travel-deals-and-tips.md";
  slug: "budget-travel-off-season-travel-deals-and-tips";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-packing-list-essentials.md": {
	id: "budget-travel-packing-list-essentials.md";
  slug: "budget-travel-packing-list-essentials";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-packing-list-the-ultimate-guide.md": {
	id: "budget-travel-packing-list-the-ultimate-guide.md";
  slug: "budget-travel-packing-list-the-ultimate-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-privacy-policy.md": {
	id: "budget-travel-privacy-policy.md";
  slug: "budget-travel-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-solo-complete-safety-guide.md": {
	id: "budget-travel-solo-complete-safety-guide.md";
  slug: "budget-travel-solo-complete-safety-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-solo-female-travel-safety-tips-europe.md": {
	id: "budget-travel-solo-female-travel-safety-tips-europe.md";
  slug: "budget-travel-solo-female-travel-safety-tips-europe";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-step-by-step-guide-to-budget-travel.md": {
	id: "budget-travel-step-by-step-guide-to-budget-travel.md";
  slug: "budget-travel-step-by-step-guide-to-budget-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-terms-of-service.md": {
	id: "budget-travel-terms-of-service.md";
  slug: "budget-travel-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-the-definitive-handbook.md": {
	id: "budget-travel-the-definitive-handbook.md";
  slug: "budget-travel-the-definitive-handbook";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-tips-for-solo-travelers.md": {
	id: "budget-travel-tips-for-solo-travelers.md";
  slug: "budget-travel-tips-for-solo-travelers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-tips-for-students.md": {
	id: "budget-travel-tips-for-students.md";
  slug: "budget-travel-tips-for-students";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-tips-that-experts-use.md": {
	id: "budget-travel-tips-that-experts-use.md";
  slug: "budget-travel-tips-that-experts-use";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-top-10-budget-destinations-for-2026.md": {
	id: "budget-travel-top-10-budget-destinations-for-2026.md";
  slug: "budget-travel-top-10-budget-destinations-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-top-10-tools-and-resources.md": {
	id: "budget-travel-top-10-tools-and-resources.md";
  slug: "budget-travel-top-10-tools-and-resources";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-travel-insurance-is-it-worth-the-money.md": {
	id: "budget-travel-travel-insurance-is-it-worth-the-money.md";
  slug: "budget-travel-travel-insurance-is-it-worth-the-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-ultimate-guide-to-budget-travel.md": {
	id: "budget-travel-ultimate-guide-to-budget-travel.md";
  slug: "budget-travel-ultimate-guide-to-budget-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-what-beginners-should-know-about-budget-travel.md": {
	id: "budget-travel-what-beginners-should-know-about-budget-travel.md";
  slug: "budget-travel-what-beginners-should-know-about-budget-travel";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"budget-travel-why-tips-forum.md": {
	id: "budget-travel-why-tips-forum.md";
  slug: "budget-travel-why-tips-forum";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-aave-vs-compound-defi-lending-giants-compared.md": {
	id: "crypto-investing-aave-vs-compound-defi-lending-giants-compared.md";
  slug: "crypto-investing-aave-vs-compound-defi-lending-giants-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-about.md": {
	id: "crypto-investing-about.md";
  slug: "crypto-investing-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-analytics-tools.md": {
	id: "crypto-investing-best-crypto-analytics-tools.md";
  slug: "crypto-investing-best-crypto-analytics-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-books-for-investors.md": {
	id: "crypto-investing-best-crypto-books-for-investors.md";
  slug: "crypto-investing-best-crypto-books-for-investors";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-exchanges-compared-for-2026.md": {
	id: "crypto-investing-best-crypto-exchanges-compared-for-2026.md";
  slug: "crypto-investing-best-crypto-exchanges-compared-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-exchanges-for-beginners.md": {
	id: "crypto-investing-best-crypto-exchanges-for-beginners.md";
  slug: "crypto-investing-best-crypto-exchanges-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-trading-strategies-for-2026.md": {
	id: "crypto-investing-best-crypto-trading-strategies-for-2026.md";
  slug: "crypto-investing-best-crypto-trading-strategies-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-crypto-wallets-for-investors.md": {
	id: "crypto-investing-best-crypto-wallets-for-investors.md";
  slug: "crypto-investing-best-crypto-wallets-for-investors";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-cryptocurrencies-to-invest-in-2026.md": {
	id: "crypto-investing-best-cryptocurrencies-to-invest-in-2026.md";
  slug: "crypto-investing-best-cryptocurrencies-to-invest-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-cryptocurrency-to-invest-in-2026-for-beginners.md": {
	id: "crypto-investing-best-cryptocurrency-to-invest-in-2026-for-beginners.md";
  slug: "crypto-investing-best-cryptocurrency-to-invest-in-2026-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-defi-lending-platforms-compared-2026.md": {
	id: "crypto-investing-best-defi-lending-platforms-compared-2026.md";
  slug: "crypto-investing-best-defi-lending-platforms-compared-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-hardware-wallets-compared-for-2026.md": {
	id: "crypto-investing-best-hardware-wallets-compared-for-2026.md";
  slug: "crypto-investing-best-hardware-wallets-compared-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-long-term-crypto-holds-2026.md": {
	id: "crypto-investing-best-long-term-crypto-holds-2026.md";
  slug: "crypto-investing-best-long-term-crypto-holds-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-best-time-to-buy-bitcoin-timing-the-market.md": {
	id: "crypto-investing-best-time-to-buy-bitcoin-timing-the-market.md";
  slug: "crypto-investing-best-time-to-buy-bitcoin-timing-the-market";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-etf-explained-how-to-invest-without-buying-btc-directly.md": {
	id: "crypto-investing-bitcoin-etf-explained-how-to-invest-without-buying-btc-directly.md";
  slug: "crypto-investing-bitcoin-etf-explained-how-to-invest-without-buying-btc-directly";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-halving-2028-the-complete-investor-s-guide.md": {
	id: "crypto-investing-bitcoin-halving-2028-the-complete-investor-s-guide.md";
  slug: "crypto-investing-bitcoin-halving-2028-the-complete-investor-s-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-hardware-wallet-comparison-2026.md": {
	id: "crypto-investing-bitcoin-hardware-wallet-comparison-2026.md";
  slug: "crypto-investing-bitcoin-hardware-wallet-comparison-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-lightning-network-fast-cheap-payments-explained.md": {
	id: "crypto-investing-bitcoin-lightning-network-fast-cheap-payments-explained.md";
  slug: "crypto-investing-bitcoin-lightning-network-fast-cheap-payments-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-vs-ethereum-investment-comparison.md": {
	id: "crypto-investing-bitcoin-vs-ethereum-investment-comparison.md";
  slug: "crypto-investing-bitcoin-vs-ethereum-investment-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-bitcoin-vs-ethereum-which-is-the-better-investment.md": {
	id: "crypto-investing-bitcoin-vs-ethereum-which-is-the-better-investment.md";
  slug: "crypto-investing-bitcoin-vs-ethereum-which-is-the-better-investment";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-chainlink-oracle-network-utility-and-investment-case.md": {
	id: "crypto-investing-chainlink-oracle-network-utility-and-investment-case.md";
  slug: "crypto-investing-chainlink-oracle-network-utility-and-investment-case";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-dollar-cost-averaging-strategy.md": {
	id: "crypto-investing-crypto-dollar-cost-averaging-strategy.md";
  slug: "crypto-investing-crypto-dollar-cost-averaging-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-etf-explained-for-beginners.md": {
	id: "crypto-investing-crypto-etf-explained-for-beginners.md";
  slug: "crypto-investing-crypto-etf-explained-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-grid-trading-bot-setup-guide-2026.md": {
	id: "crypto-investing-crypto-grid-trading-bot-setup-guide-2026.md";
  slug: "crypto-investing-crypto-grid-trading-bot-setup-guide-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-market-cycles-how-to-time-your-investments.md": {
	id: "crypto-investing-crypto-market-cycles-how-to-time-your-investments.md";
  slug: "crypto-investing-crypto-market-cycles-how-to-time-your-investments";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-portfolio-rebalancing-tools.md": {
	id: "crypto-investing-crypto-portfolio-rebalancing-tools.md";
  slug: "crypto-investing-crypto-portfolio-rebalancing-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-security-best-practices-protect-your-assets.md": {
	id: "crypto-investing-crypto-security-best-practices-protect-your-assets.md";
  slug: "crypto-investing-crypto-security-best-practices-protect-your-assets";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-staking-explained-how-to-earn-passive-income.md": {
	id: "crypto-investing-crypto-staking-explained-how-to-earn-passive-income.md";
  slug: "crypto-investing-crypto-staking-explained-how-to-earn-passive-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-swing-trading-vs-day-trading-which-is-better.md": {
	id: "crypto-investing-crypto-swing-trading-vs-day-trading-which-is-better.md";
  slug: "crypto-investing-crypto-swing-trading-vs-day-trading-which-is-better";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-tax-guide-what-you-need-to-know.md": {
	id: "crypto-investing-crypto-tax-guide-what-you-need-to-know.md";
  slug: "crypto-investing-crypto-tax-guide-what-you-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-tax-loss-harvesting-the-ultimate-guide.md": {
	id: "crypto-investing-crypto-tax-loss-harvesting-the-ultimate-guide.md";
  slug: "crypto-investing-crypto-tax-loss-harvesting-the-ultimate-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-crypto-technical-analysis-reading-charts-like-a-pro.md": {
	id: "crypto-investing-crypto-technical-analysis-reading-charts-like-a-pro.md";
  slug: "crypto-investing-crypto-technical-analysis-reading-charts-like-a-pro";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-defi-investing-opportunities-2026.md": {
	id: "crypto-investing-defi-investing-opportunities-2026.md";
  slug: "crypto-investing-defi-investing-opportunities-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-defi-yield-farming-risks-and-rewards-explained.md": {
	id: "crypto-investing-defi-yield-farming-risks-and-rewards-explained.md";
  slug: "crypto-investing-defi-yield-farming-risks-and-rewards-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-dogecoin-vs-shiba-inu-vs-pepe-memecoin-comparison.md": {
	id: "crypto-investing-dogecoin-vs-shiba-inu-vs-pepe-memecoin-comparison.md";
  slug: "crypto-investing-dogecoin-vs-shiba-inu-vs-pepe-memecoin-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-dollar-cost-averaging-crypto-does-it-work.md": {
	id: "crypto-investing-dollar-cost-averaging-crypto-does-it-work.md";
  slug: "crypto-investing-dollar-cost-averaging-crypto-does-it-work";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-dollar-cost-averaging-crypto-strategy.md": {
	id: "crypto-investing-dollar-cost-averaging-crypto-strategy.md";
  slug: "crypto-investing-dollar-cost-averaging-crypto-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-dollar-cost-averaging-vs-lump-sum-crypto-investing.md": {
	id: "crypto-investing-dollar-cost-averaging-vs-lump-sum-crypto-investing.md";
  slug: "crypto-investing-dollar-cost-averaging-vs-lump-sum-crypto-investing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-during-bear-markets.md": {
	id: "crypto-investing-during-bear-markets.md";
  slug: "crypto-investing-during-bear-markets";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-for-retirement.md": {
	id: "crypto-investing-for-retirement.md";
  slug: "crypto-investing-for-retirement";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-hardware-wallet-vs-software-wallet-complete-comparison.md": {
	id: "crypto-investing-hardware-wallet-vs-software-wallet-complete-comparison.md";
  slug: "crypto-investing-hardware-wallet-vs-software-wallet-complete-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-build-a-crypto-portfolio.md": {
	id: "crypto-investing-how-to-build-a-crypto-portfolio.md";
  slug: "crypto-investing-how-to-build-a-crypto-portfolio";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-create-a-crypto-investment-plan.md": {
	id: "crypto-investing-how-to-create-a-crypto-investment-plan.md";
  slug: "crypto-investing-how-to-create-a-crypto-investment-plan";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-diversify-crypto-portfolio.md": {
	id: "crypto-investing-how-to-diversify-crypto-portfolio.md";
  slug: "crypto-investing-how-to-diversify-crypto-portfolio";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-find-new-memecoins-before-they-moon.md": {
	id: "crypto-investing-how-to-find-new-memecoins-before-they-moon.md";
  slug: "crypto-investing-how-to-find-new-memecoins-before-they-moon";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-invest-in-crypto-safely.md": {
	id: "crypto-investing-how-to-invest-in-crypto-safely.md";
  slug: "crypto-investing-how-to-invest-in-crypto-safely";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-invest-in-layer-2-tokens.md": {
	id: "crypto-investing-how-to-invest-in-layer-2-tokens.md";
  slug: "crypto-investing-how-to-invest-in-layer-2-tokens";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-read-crypto-charts-for-beginners.md": {
	id: "crypto-investing-how-to-read-crypto-charts-for-beginners.md";
  slug: "crypto-investing-how-to-read-crypto-charts-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-read-crypto-charts-technical-analysis-basics.md": {
	id: "crypto-investing-how-to-read-crypto-charts-technical-analysis-basics.md";
  slug: "crypto-investing-how-to-read-crypto-charts-technical-analysis-basics";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-research-altcoins-before-investing.md": {
	id: "crypto-investing-how-to-research-altcoins-before-investing.md";
  slug: "crypto-investing-how-to-research-altcoins-before-investing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-set-crypto-price-alerts.md": {
	id: "crypto-investing-how-to-set-crypto-price-alerts.md";
  slug: "crypto-investing-how-to-set-crypto-price-alerts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-spot-crypto-bull-runs-early.md": {
	id: "crypto-investing-how-to-spot-crypto-bull-runs-early.md";
  slug: "crypto-investing-how-to-spot-crypto-bull-runs-early";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-spot-crypto-scams-red-flags-to-watch.md": {
	id: "crypto-investing-how-to-spot-crypto-scams-red-flags-to-watch.md";
  slug: "crypto-investing-how-to-spot-crypto-scams-red-flags-to-watch";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-stake-ethereum-complete-beginner-s-guide.md": {
	id: "crypto-investing-how-to-stake-ethereum-complete-beginner-s-guide.md";
  slug: "crypto-investing-how-to-stake-ethereum-complete-beginner-s-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-start-investing-in-crypto-complete-guide.md": {
	id: "crypto-investing-how-to-start-investing-in-crypto-complete-guide.md";
  slug: "crypto-investing-how-to-start-investing-in-crypto-complete-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-start-investing-in-crypto.md": {
	id: "crypto-investing-how-to-start-investing-in-crypto.md";
  slug: "crypto-investing-how-to-start-investing-in-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-how-to-store-cryptocurrency-safely-wallet-guide.md": {
	id: "crypto-investing-how-to-store-cryptocurrency-safely-wallet-guide.md";
  slug: "crypto-investing-how-to-store-cryptocurrency-safely-wallet-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-institutional-trends.md": {
	id: "crypto-investing-institutional-trends.md";
  slug: "crypto-investing-institutional-trends";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-is-cryptocurrency-a-good-investment-in-2026.md": {
	id: "crypto-investing-is-cryptocurrency-a-good-investment-in-2026.md";
  slug: "crypto-investing-is-cryptocurrency-a-good-investment-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-layer-2-ethereum-arbitrum-vs-optimism-vs-base-compared.md": {
	id: "crypto-investing-layer-2-ethereum-arbitrum-vs-optimism-vs-base-compared.md";
  slug: "crypto-investing-layer-2-ethereum-arbitrum-vs-optimism-vs-base-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-mistakes-to-avoid.md": {
	id: "crypto-investing-mistakes-to-avoid.md";
  slug: "crypto-investing-mistakes-to-avoid";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-nft-investing-guide-beyond-the-hype.md": {
	id: "crypto-investing-nft-investing-guide-beyond-the-hype.md";
  slug: "crypto-investing-nft-investing-guide-beyond-the-hype";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-passive-income-with-crypto-staking.md": {
	id: "crypto-investing-passive-income-with-crypto-staking.md";
  slug: "crypto-investing-passive-income-with-crypto-staking";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-privacy-policy.md": {
	id: "crypto-investing-privacy-policy.md";
  slug: "crypto-investing-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-risk-management-in-crypto-investing.md": {
	id: "crypto-investing-risk-management-in-crypto-investing.md";
  slug: "crypto-investing-risk-management-in-crypto-investing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-solana-vs-ethereum-vs-avalanche-deep-comparison.md": {
	id: "crypto-investing-solana-vs-ethereum-vs-avalanche-deep-comparison.md";
  slug: "crypto-investing-solana-vs-ethereum-vs-avalanche-deep-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-tax-implications.md": {
	id: "crypto-investing-tax-implications.md";
  slug: "crypto-investing-tax-implications";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-terms-of-service.md": {
	id: "crypto-investing-terms-of-service.md";
  slug: "crypto-investing-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-top-10-altcoins-to-watch-in-2026.md": {
	id: "crypto-investing-top-10-altcoins-to-watch-in-2026.md";
  slug: "crypto-investing-top-10-altcoins-to-watch-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-top-10-altcoins-with-the-most-potential-in-2026.md": {
	id: "crypto-investing-top-10-altcoins-with-the-most-potential-in-2026.md";
  slug: "crypto-investing-top-10-altcoins-with-the-most-potential-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-top-5-crypto-mistakes-beginners-make.md": {
	id: "crypto-investing-top-5-crypto-mistakes-beginners-make.md";
  slug: "crypto-investing-top-5-crypto-mistakes-beginners-make";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-understanding-bitcoin-halving-impact.md": {
	id: "crypto-investing-understanding-bitcoin-halving-impact.md";
  slug: "crypto-investing-understanding-bitcoin-halving-impact";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-understanding-crypto-market-cap.md": {
	id: "crypto-investing-understanding-crypto-market-cap.md";
  slug: "crypto-investing-understanding-crypto-market-cap";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-understanding-crypto-market-cycles.md": {
	id: "crypto-investing-understanding-crypto-market-cycles.md";
  slug: "crypto-investing-understanding-crypto-market-cycles";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-understanding-crypto-on-chain-analysis.md": {
	id: "crypto-investing-understanding-crypto-on-chain-analysis.md";
  slug: "crypto-investing-understanding-crypto-on-chain-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-understanding-crypto-tokenomics.md": {
	id: "crypto-investing-understanding-crypto-tokenomics.md";
  slug: "crypto-investing-understanding-crypto-tokenomics";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-uniswap-v4-new-features-what-you-need-to-know.md": {
	id: "crypto-investing-uniswap-v4-new-features-what-you-need-to-know.md";
  slug: "crypto-investing-uniswap-v4-new-features-what-you-need-to-know";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-vs-stock-market.md": {
	id: "crypto-investing-vs-stock-market.md";
  slug: "crypto-investing-vs-stock-market";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-what-is-blockchain-complete-beginner-explanation.md": {
	id: "crypto-investing-what-is-blockchain-complete-beginner-explanation.md";
  slug: "crypto-investing-what-is-blockchain-complete-beginner-explanation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-when-to-buy-altcoins-timing-and-strategy-guide.md": {
	id: "crypto-investing-when-to-buy-altcoins-timing-and-strategy-guide.md";
  slug: "crypto-investing-when-to-buy-altcoins-timing-and-strategy-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-investing-with-small-amounts.md": {
	id: "crypto-investing-with-small-amounts.md";
  slug: "crypto-investing-with-small-amounts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-about.md": {
	id: "crypto-trading-about.md";
  slug: "crypto-trading-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-books.md": {
	id: "crypto-trading-best-books.md";
  slug: "crypto-trading-best-books";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-bots.md": {
	id: "crypto-trading-best-bots.md";
  slug: "crypto-trading-best-bots";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-communities.md": {
	id: "crypto-trading-best-communities.md";
  slug: "crypto-trading-best-communities";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-crypto-pairs-to-trade.md": {
	id: "crypto-trading-best-crypto-pairs-to-trade.md";
  slug: "crypto-trading-best-crypto-pairs-to-trade";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-indicators.md": {
	id: "crypto-trading-best-indicators.md";
  slug: "crypto-trading-best-indicators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-platforms-2026.md": {
	id: "crypto-trading-best-platforms-2026.md";
  slug: "crypto-trading-best-platforms-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-strategies-2026.md": {
	id: "crypto-trading-best-strategies-2026.md";
  slug: "crypto-trading-best-strategies-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-technical-indicators-for-crypto-trading.md": {
	id: "crypto-trading-best-technical-indicators-for-crypto-trading.md";
  slug: "best-technical-indicators-for-crypto-trading-a-practical-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-timeframes-for-analysis.md": {
	id: "crypto-trading-best-timeframes-for-analysis.md";
  slug: "best-timeframes-for-crypto-trading-analysis-a-complete-guide-for-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-best-tools-free.md": {
	id: "crypto-trading-best-tools-free.md";
  slug: "crypto-trading-best-tools-free";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-blockchain-oracle-platforms-comparison.md": {
	id: "crypto-trading-blockchain-oracle-platforms-comparison.md";
  slug: "crypto-trading-blockchain-oracle-platforms-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-bollinger-bands-crypto-strategy.md": {
	id: "crypto-trading-bollinger-bands-crypto-strategy.md";
  slug: "crypto-trading-bollinger-bands-crypto-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-credit-card-points-for-travel-complete-beginner-guide.md": {
	id: "crypto-trading-credit-card-points-for-travel-complete-beginner-guide.md";
  slug: "crypto-trading-credit-card-points-for-travel-complete-beginner-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-arbitrage-trading-strategies-explained.md": {
	id: "crypto-trading-crypto-arbitrage-trading-strategies-explained.md";
  slug: "crypto-arbitrage-trading-strategies-explained-your-complete-guide-to-profiting-f";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-basis-trading-strategies.md": {
	id: "crypto-trading-crypto-basis-trading-strategies.md";
  slug: "crypto-trading-crypto-basis-trading-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-breakout-trading-strategies.md": {
	id: "crypto-trading-crypto-breakout-trading-strategies.md";
  slug: "crypto-breakout-trading-strategies-a-complete-guide-to-catching-major-moves";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-breakout-trading-strategy.md": {
	id: "crypto-trading-crypto-breakout-trading-strategy.md";
  slug: "crypto-trading-crypto-breakout-trading-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-correlation-trading.md": {
	id: "crypto-trading-crypto-correlation-trading.md";
  slug: "crypto-trading-crypto-correlation-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-day-trading-for-beginners.md": {
	id: "crypto-trading-crypto-day-trading-for-beginners.md";
  slug: "crypto-trading-crypto-day-trading-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-dca-vs-lump-sum.md": {
	id: "crypto-trading-crypto-dca-vs-lump-sum.md";
  slug: "crypto-trading-crypto-dca-vs-lump-sum";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-derivatives-trading-futures-and-options-guide.md": {
	id: "crypto-trading-crypto-derivatives-trading-futures-and-options-guide.md";
  slug: "crypto-derivatives-trading-a-complete-guide-to-futures-and-options-in-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-funding-rate-arbitrage.md": {
	id: "crypto-trading-crypto-funding-rate-arbitrage.md";
  slug: "crypto-trading-crypto-funding-rate-arbitrage";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-grid-trading-bots.md": {
	id: "crypto-trading-crypto-grid-trading-bots.md";
  slug: "crypto-trading-crypto-grid-trading-bots";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-margin-trading-risks.md": {
	id: "crypto-trading-crypto-margin-trading-risks.md";
  slug: "crypto-trading-crypto-margin-trading-risks";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-market-order-types-explained.md": {
	id: "crypto-trading-crypto-market-order-types-explained.md";
  slug: "crypto-trading-crypto-market-order-types-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-mean-reversion-trading-strategies.md": {
	id: "crypto-trading-crypto-mean-reversion-trading-strategies.md";
  slug: "crypto-mean-reversion-trading-strategies-a-complete-guide-for-profiting-from-mar";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-options-trading-for-beginners.md": {
	id: "crypto-trading-crypto-options-trading-for-beginners.md";
  slug: "crypto-trading-crypto-options-trading-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-order-book-analysis-how-to-read-and-trade-using-depth-charts-and-level-2-.md": {
	id: "crypto-trading-crypto-order-book-analysis-how-to-read-and-trade-using-depth-charts-and-level-2-.md";
  slug: "crypto-order-book-analysis-how-to-read-and-trade-using-depth-charts-and-level-2-";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-perpetual-futures-guide.md": {
	id: "crypto-trading-crypto-perpetual-futures-guide.md";
  slug: "crypto-trading-crypto-perpetual-futures-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-portfolio-diversification-strategies-how-to-build-a-balanced-crypto-portf.md": {
	id: "crypto-trading-crypto-portfolio-diversification-strategies-how-to-build-a-balanced-crypto-portf.md";
  slug: "crypto-portfolio-diversification-strategies-how-to-build-a-balanced-crypto-portf";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-portfoliorebalancing-guide.md": {
	id: "crypto-trading-crypto-portfoliorebalancing-guide.md";
  slug: "crypto-trading-crypto-portfoliorebalancing-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-position-sizing-and-portfolio-allocation.md": {
	id: "crypto-trading-crypto-position-sizing-and-portfolio-allocation.md";
  slug: "crypto-position-sizing-and-portfolio-allocation-the-complete-guide-for-smart-tra";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-range-trading-strategy.md": {
	id: "crypto-trading-crypto-range-trading-strategy.md";
  slug: "crypto-trading-crypto-range-trading-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-scalping-strategies-explained.md": {
	id: "crypto-trading-crypto-scalping-strategies-explained.md";
  slug: "crypto-trading-crypto-scalping-strategies-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-swing-trading-fundamentals.md": {
	id: "crypto-trading-crypto-swing-trading-fundamentals.md";
  slug: "crypto-trading-crypto-swing-trading-fundamentals";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-swing-trading-guide.md": {
	id: "crypto-trading-crypto-swing-trading-guide.md";
  slug: "crypto-trading-crypto-swing-trading-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-crypto-tax-loss-harvesting.md": {
	id: "crypto-trading-crypto-tax-loss-harvesting.md";
  slug: "crypto-trading-crypto-tax-loss-harvesting";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-dollar-cost-averaging-crypto-strategy-complete-guide.md": {
	id: "crypto-trading-dollar-cost-averaging-crypto-strategy-complete-guide.md";
  slug: "dollar-cost-averaging-crypto-strategy-the-complete-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-elliott-wave-crypto-analysis.md": {
	id: "crypto-trading-elliott-wave-crypto-analysis.md";
  slug: "crypto-trading-elliott-wave-crypto-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-fibonacci-retracement-crypto.md": {
	id: "crypto-trading-fibonacci-retracement-crypto.md";
  slug: "crypto-trading-fibonacci-retracement-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-fibonacci-retracement-in-complete-guide-to-using-golden-ratio-lev.md": {
	id: "crypto-trading-fibonacci-retracement-in-complete-guide-to-using-golden-ratio-lev.md";
  slug: "fibonacci-retracement-in-crypto-trading-complete-guide-to-using-golden-ratio-lev";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-grid-trading-bot-crypto-how-it-works.md": {
	id: "crypto-trading-grid-trading-bot-crypto-how-it-works.md";
  slug: "grid-trading-bot-crypto-how-it-works";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-backtest-crypto-strategies.md": {
	id: "crypto-trading-how-to-backtest-crypto-strategies.md";
  slug: "crypto-trading-how-to-backtest-crypto-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-build-a-trading-plan.md": {
	id: "crypto-trading-how-to-build-a-trading-plan.md";
  slug: "crypto-trading-how-to-build-a-trading-plan";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-paper-trade-crypto.md": {
	id: "crypto-trading-how-to-paper-trade-crypto.md";
  slug: "crypto-trading-how-to-paper-trade-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-read-crypto-candlestick-charts.md": {
	id: "crypto-trading-how-to-read-crypto-candlestick-charts.md";
  slug: "crypto-trading-how-to-read-crypto-candlestick-charts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-set-stop-losses-crypto.md": {
	id: "crypto-trading-how-to-set-stop-losses-crypto.md";
  slug: "crypto-trading-how-to-set-stop-losses-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-start-with-100.md": {
	id: "crypto-trading-how-to-start-with-100.md";
  slug: "crypto-trading-how-to-start-with-100";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-trade-crypto-futures.md": {
	id: "crypto-trading-how-to-trade-crypto-futures.md";
  slug: "crypto-trading-how-to-trade-crypto-futures";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-trade-crypto-news-events.md": {
	id: "crypto-trading-how-to-trade-crypto-news-events.md";
  slug: "crypto-trading-how-to-trade-crypto-news-events";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-travel-during-peak-season-without-breaking-the-bank.md": {
	id: "crypto-trading-how-to-travel-during-peak-season-without-breaking-the-bank.md";
  slug: "crypto-trading-how-to-travel-during-peak-season-without-breaking-the-bank";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-how-to-use-moving-averages-in-crypto-trading.md": {
	id: "crypto-trading-how-to-use-moving-averages-in-crypto-trading.md";
  slug: "how-to-use-moving-averages-in-crypto-trading-a-complete-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-ichimoku-cloud-crypto-trading.md": {
	id: "crypto-trading-ichimoku-cloud-crypto-trading.md";
  slug: "crypto-trading-ichimoku-cloud-crypto-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-journal-template.md": {
	id: "crypto-trading-journal-template.md";
  slug: "crypto-trading-journal-template";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-macd-strategy.md": {
	id: "crypto-trading-macd-strategy.md";
  slug: "crypto-trading-macd-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-mistakes-beginners-make.md": {
	id: "crypto-trading-mistakes-beginners-make.md";
  slug: "crypto-trading-mistakes-beginners-make";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-moving-averages-crypto-trading.md": {
	id: "crypto-trading-moving-averages-crypto-trading.md";
  slug: "crypto-trading-moving-averages-crypto-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-position-sizing-in-crypto-trading.md": {
	id: "crypto-trading-position-sizing-in-crypto-trading.md";
  slug: "crypto-trading-position-sizing-in-crypto-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-privacy-policy.md": {
	id: "crypto-trading-privacy-policy.md";
  slug: "crypto-trading-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-psychology.md": {
	id: "crypto-trading-psychology.md";
  slug: "crypto-trading-psychology";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-risk-management-in-crypto-trading.md": {
	id: "crypto-trading-risk-management-in-crypto-trading.md";
  slug: "crypto-trading-risk-management-in-crypto-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-risk-management-strategies-for-crypto-trading.md": {
	id: "crypto-trading-risk-management-strategies-for-crypto-trading.md";
  slug: "risk-management-strategies-for-crypto-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-rsi-trading-strategy-crypto.md": {
	id: "crypto-trading-rsi-trading-strategy-crypto.md";
  slug: "crypto-trading-rsi-trading-strategy-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-scalping-cryptocurrency-tips-and-strategies.md": {
	id: "crypto-trading-scalping-cryptocurrency-tips-and-strategies.md";
  slug: "crypto-scalping-a-complete-guide-to-high-frequency-day-trading-in-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-supertrend-crypto-strategy.md": {
	id: "crypto-trading-supertrend-crypto-strategy.md";
  slug: "crypto-trading-supertrend-crypto-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-support-and-resistance-levels-crypto-trading.md": {
	id: "crypto-trading-support-and-resistance-levels-crypto-trading.md";
  slug: "support-and-resistance-levels-crypto-trading-the-complete-guide-for-maximizing-y";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-support-and-resistance-levels-crypto.md": {
	id: "crypto-trading-support-and-resistance-levels-crypto.md";
  slug: "crypto-trading-support-and-resistance-levels-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-swing-trading-cryptocurrency-for-beginners.md": {
	id: "crypto-trading-swing-trading-cryptocurrency-for-beginners.md";
  slug: "swing-trading-cryptocurrency-for-beginners-the-complete-2024-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-terms-of-service.md": {
	id: "crypto-trading-terms-of-service.md";
  slug: "crypto-trading-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-trading-psychology-for-cryptocurrency-traders.md": {
	id: "crypto-trading-trading-psychology-for-cryptocurrency-traders.md";
  slug: "trading-psychology-for-cryptocurrency-traders-master-your-mind-to-master-the-mar";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-understanding-crypto-order-books.md": {
	id: "crypto-trading-understanding-crypto-order-books.md";
  slug: "crypto-trading-understanding-crypto-order-books";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-volume-analysis-in-crypto.md": {
	id: "crypto-trading-volume-analysis-in-crypto.md";
  slug: "crypto-trading-volume-analysis-in-crypto";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"crypto-trading-vwap-strategy.md": {
	id: "crypto-trading-vwap-strategy.md";
  slug: "crypto-trading-vwap-strategy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-about.md": {
	id: "defi-yield-about.md";
  slug: "defi-yield-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-aggregators.md": {
	id: "defi-yield-best-defi-aggregators.md";
  slug: "defi-yield-best-defi-aggregators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-analytics-platforms-compared.md": {
	id: "defi-yield-best-defi-analytics-platforms-compared.md";
  slug: "defi-yield-best-defi-analytics-platforms-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-analytics-tools.md": {
	id: "defi-yield-best-defi-analytics-tools.md";
  slug: "defi-yield-best-defi-analytics-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-auto-compound-tools.md": {
	id: "defi-yield-best-defi-auto-compound-tools.md";
  slug: "defi-yield-best-defi-auto-compound-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-compounding-strategies.md": {
	id: "defi-yield-best-defi-compounding-strategies.md";
  slug: "defi-yield-best-defi-compounding-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-crypto-index-funds.md": {
	id: "defi-yield-best-defi-crypto-index-funds.md";
  slug: "defi-yield-best-defi-crypto-index-funds";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-dashboards-and-trackers.md": {
	id: "defi-yield-best-defi-dashboards-and-trackers.md";
  slug: "defi-yield-best-defi-dashboards-and-trackers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-education-resources.md": {
	id: "defi-yield-best-defi-education-resources.md";
  slug: "defi-yield-best-defi-education-resources";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-gas-optimization-tips.md": {
	id: "defi-yield-best-defi-gas-optimization-tips.md";
  slug: "defi-yield-best-defi-gas-optimization-tips";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-insurance-coverage-options.md": {
	id: "defi-yield-best-defi-insurance-coverage-options.md";
  slug: "defi-yield-best-defi-insurance-coverage-options";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-leverage-farming-strategies.md": {
	id: "defi-yield-best-defi-leverage-farming-strategies.md";
  slug: "defi-yield-best-defi-leverage-farming-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-platforms-for-beginners.md": {
	id: "defi-yield-best-defi-platforms-for-beginners.md";
  slug: "defi-yield-best-defi-platforms-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-podcasts-and-resources.md": {
	id: "defi-yield-best-defi-podcasts-and-resources.md";
  slug: "defi-yield-best-defi-podcasts-and-resources";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-risk-management-tools.md": {
	id: "defi-yield-best-defi-risk-management-tools.md";
  slug: "defi-yield-best-defi-risk-management-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-savings-account-alternatives.md": {
	id: "defi-yield-best-defi-savings-account-alternatives.md";
  slug: "defi-yield-best-defi-savings-account-alternatives";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-staking-rewards.md": {
	id: "defi-yield-best-defi-staking-rewards.md";
  slug: "best-defi-staking-rewards-the-ultimate-guide-to-maximizing-your-yield-in-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-strategies-for-bear-markets.md": {
	id: "defi-yield-best-defi-strategies-for-bear-markets.md";
  slug: "defi-yield-best-defi-strategies-for-bear-markets";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-sustainable-apy-range.md": {
	id: "defi-yield-best-defi-sustainable-apy-range.md";
  slug: "defi-yield-best-defi-sustainable-apy-range";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-tokens-to-watch-2026.md": {
	id: "defi-yield-best-defi-tokens-to-watch-2026.md";
  slug: "defi-yield-best-defi-tokens-to-watch-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-wallets-2026.md": {
	id: "defi-yield-best-defi-wallets-2026.md";
  slug: "best-defi-wallets-2026-complete-guide-to-secure-decentralized-finance-storage";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-defi-year-in-review-2025.md": {
	id: "defi-yield-best-defi-year-in-review-2025.md";
  slug: "defi-yield-best-defi-year-in-review-2025";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-farming-platforms-2026.md": {
	id: "defi-yield-best-farming-platforms-2026.md";
  slug: "best-defi-yield-farming-platforms-2026-the-ultimate-guide-to-maximizing-your-cry";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-hunting-strategies.md": {
	id: "defi-yield-best-hunting-strategies.md";
  slug: "defi-yield-best-hunting-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-optimizer-protocols.md": {
	id: "defi-yield-best-optimizer-protocols.md";
  slug: "defi-yield-best-optimizer-protocols";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-stablecoin-defi-strategies.md": {
	id: "defi-yield-best-stablecoin-defi-strategies.md";
  slug: "defi-yield-best-stablecoin-defi-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-best-yield-farming-strategies.md": {
	id: "defi-yield-best-yield-farming-strategies.md";
  slug: "defi-yield-best-yield-farming-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-budget-travel-packing-list-the-ultimate-guide.md": {
	id: "defi-yield-budget-travel-packing-list-the-ultimate-guide.md";
  slug: "defi-yield-budget-travel-packing-list-the-ultimate-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-cross-chain-defi-explained.md": {
	id: "defi-yield-cross-chain-defi-explained.md";
  slug: "defi-yield-cross-chain-defi-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-6-vs-defi-farming-compared.md": {
	id: "defi-yield-defi-6-vs-defi-farming-compared.md";
  slug: "defi-yield-defi-6-vs-defi-farming-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-arbitrage-opportunities-2026.md": {
	id: "defi-yield-defi-arbitrage-opportunities-2026.md";
  slug: "defi-yield-defi-arbitrage-opportunities-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-composability-explained.md": {
	id: "defi-yield-defi-composability-explained.md";
  slug: "defi-yield-defi-composability-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-cross-chain-bridges-compared.md": {
	id: "defi-yield-defi-cross-chain-bridges-compared.md";
  slug: "defi-yield-defi-cross-chain-bridges-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-farming-tax-reporting-guide.md": {
	id: "defi-yield-defi-farming-tax-reporting-guide.md";
  slug: "defi-yield-defi-farming-tax-reporting-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-flash-loans-explained.md": {
	id: "defi-yield-defi-flash-loans-explained.md";
  slug: "defi-yield-defi-flash-loans-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-hack-prevention-guide.md": {
	id: "defi-yield-defi-hack-prevention-guide.md";
  slug: "defi-yield-defi-hack-prevention-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-impermanent-loss-calculator-tools.md": {
	id: "defi-yield-defi-impermanent-loss-calculator-tools.md";
  slug: "defi-yield-defi-impermanent-loss-calculator-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-insurance-protocols.md": {
	id: "defi-yield-defi-insurance-protocols.md";
  slug: "defi-yield-defi-insurance-protocols";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-lending-platforms-compared.md": {
	id: "defi-yield-defi-lending-platforms-compared.md";
  slug: "defi-lending-platforms-compared-the-ultimate-guide-to-maximizing-yield-in-2024";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-lending-vs-liquidity-mining.md": {
	id: "defi-yield-defi-lending-vs-liquidity-mining.md";
  slug: "defi-yield-defi-lending-vs-liquidity-mining";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-liquidity-pools-explained.md": {
	id: "defi-yield-defi-liquidity-pools-explained.md";
  slug: "defi-liquidity-pools-explained-the-complete-guide-to-earning-yield-in-decentrali";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-liquidity-provision-for-beginners.md": {
	id: "defi-yield-defi-liquidity-provision-for-beginners.md";
  slug: "defi-yield-defi-liquidity-provision-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-mining-vs-staking-comparison.md": {
	id: "defi-yield-defi-mining-vs-staking-comparison.md";
  slug: "defi-yield-defi-mining-vs-staking-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-options-and-derivatives-explained.md": {
	id: "defi-yield-defi-options-and-derivatives-explained.md";
  slug: "defi-yield-defi-options-and-derivatives-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-portfolio-diversification-guide.md": {
	id: "defi-yield-defi-portfolio-diversification-guide.md";
  slug: "defi-yield-defi-portfolio-diversification-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-portfolio-rebalancing-guide.md": {
	id: "defi-yield-defi-portfolio-rebalancing-guide.md";
  slug: "defi-yield-defi-portfolio-rebalancing-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-profit-taking-strategies.md": {
	id: "defi-yield-defi-profit-taking-strategies.md";
  slug: "defi-yield-defi-profit-taking-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-regulation-update-2026.md": {
	id: "defi-yield-defi-regulation-update-2026.md";
  slug: "defi-yield-defi-regulation-update-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-risks-and-how-to-mitigate-them.md": {
	id: "defi-yield-defi-risks-and-how-to-mitigate-them.md";
  slug: "defi-risks-the-ultimate-guide-to-identifying-and-mitigating-risks-in-decentraliz";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-security-best-practices-comprehensive-guide-2026.md": {
	id: "defi-yield-defi-security-best-practices-comprehensive-guide-2026.md";
  slug: "defi-security-best-practices-the-ultimate-guide-to-protecting-your-assets-in-202";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-smart-contract-risk-assessment.md": {
	id: "defi-yield-defi-smart-contract-risk-assessment.md";
  slug: "defi-yield-defi-smart-contract-risk-assessment";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-token-price-prediction-methods.md": {
	id: "defi-yield-defi-token-price-prediction-methods.md";
  slug: "defi-yield-defi-token-price-prediction-methods";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-defi-vs-cefi-comparison.md": {
	id: "defi-yield-defi-vs-cefi-comparison.md";
  slug: "defi-yield-defi-vs-cefi-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-gas-optimization-ethereum-defi.md": {
	id: "defi-yield-gas-optimization-ethereum-defi.md";
  slug: "gas-optimization-ethereum-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-audit-defi-protocols.md": {
	id: "defi-yield-how-to-audit-defi-protocols.md";
  slug: "defi-yield-how-to-audit-defi-protocols";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-bridge-crypto-to-defi.md": {
	id: "defi-yield-how-to-bridge-crypto-to-defi.md";
  slug: "";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-build-a-defi-portfolio.md": {
	id: "defi-yield-how-to-build-a-defi-portfolio.md";
  slug: "defi-yield-how-to-build-a-defi-portfolio";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-calculate-apy-vs-apr-defi.md": {
	id: "defi-yield-how-to-calculate-apy-vs-apr-defi.md";
  slug: "defi-yield-how-to-calculate-apy-vs-apr-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-calculate-defi-portfolio-value.md": {
	id: "defi-yield-how-to-calculate-defi-portfolio-value.md";
  slug: "defi-yield-how-to-calculate-defi-portfolio-value";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-calculate-net-apy-in-defi.md": {
	id: "defi-yield-how-to-calculate-net-apy-in-defi.md";
  slug: "defi-yield-how-to-calculate-net-apy-in-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-earn-btc-yield-on-defi.md": {
	id: "defi-yield-how-to-earn-btc-yield-on-defi.md";
  slug: "defi-yield-how-to-earn-btc-yield-on-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-earn-passive-income-defi.md": {
	id: "defi-yield-how-to-earn-passive-income-defi.md";
  slug: "";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-evaluate-defi-project-fundamentals.md": {
	id: "defi-yield-how-to-evaluate-defi-project-fundamentals.md";
  slug: "defi-yield-how-to-evaluate-defi-project-fundamentals";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-find-cheap-hotels-insider-strategies.md": {
	id: "defi-yield-how-to-find-cheap-hotels-insider-strategies.md";
  slug: "defi-yield-how-to-find-cheap-hotels-insider-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-find-hidden-gem-destinations-on-a-budget.md": {
	id: "defi-yield-how-to-find-hidden-gem-destinations-on-a-budget.md";
  slug: "defi-yield-how-to-find-hidden-gem-destinations-on-a-budget";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-provide-liquidity-on-curve.md": {
	id: "defi-yield-how-to-provide-liquidity-on-curve.md";
  slug: "defi-yield-how-to-provide-liquidity-on-curve";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-provide-liquidity-on-defi.md": {
	id: "defi-yield-how-to-provide-liquidity-on-defi.md";
  slug: "defi-yield-how-to-provide-liquidity-on-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-spot-defi-rug-pulls.md": {
	id: "defi-yield-how-to-spot-defi-rug-pulls.md";
  slug: "defi-yield-how-to-spot-defi-rug-pulls";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-start-defi-with-100-dollars.md": {
	id: "defi-yield-how-to-start-defi-with-100-dollars.md";
  slug: "defi-yield-how-to-start-defi-with-100-dollars";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-start-yield-farming-complete-beginner-guide-2026.md": {
	id: "defi-yield-how-to-start-yield-farming-complete-beginner-guide-2026.md";
  slug: "how-to-start-yield-farming-complete-beginners-guide-for-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-start-yield-farming.md": {
	id: "defi-yield-how-to-start-yield-farming.md";
  slug: "defi-yield-how-to-start-yield-farming";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-track-defi-tvl-trends.md": {
	id: "defi-yield-how-to-track-defi-tvl-trends.md";
  slug: "defi-yield-how-to-track-defi-tvl-trends";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-1inch-aggregator.md": {
	id: "defi-yield-how-to-use-1inch-aggregator.md";
  slug: "defi-yield-how-to-use-1inch-aggregator";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-aave-flash-loans.md": {
	id: "defi-yield-how-to-use-aave-flash-loans.md";
  slug: "defi-yield-how-to-use-aave-flash-loans";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-aave-for-borrowing.md": {
	id: "defi-yield-how-to-use-aave-for-borrowing.md";
  slug: "defi-yield-how-to-use-aave-for-borrowing";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-balancer-lp.md": {
	id: "defi-yield-how-to-use-balancer-lp.md";
  slug: "defi-yield-how-to-use-balancer-lp";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-convex-finance-for-boosted-apy.md": {
	id: "defi-yield-how-to-use-convex-finance-for-boosted-apy.md";
  slug: "defi-yield-how-to-use-convex-finance-for-boosted-apy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-curve-finance.md": {
	id: "defi-yield-how-to-use-curve-finance.md";
  slug: "defi-yield-how-to-use-curve-finance";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-makerdao-for-dai-generation.md": {
	id: "defi-yield-how-to-use-makerdao-for-dai-generation.md";
  slug: "defi-yield-how-to-use-makerdao-for-dai-generation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-paraswap-swap-aggregation.md": {
	id: "defi-yield-how-to-use-paraswap-swap-aggregation.md";
  slug: "defi-yield-how-to-use-paraswap-swap-aggregation";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-sushiswap-farming.md": {
	id: "defi-yield-how-to-use-sushiswap-farming.md";
  slug: "defi-yield-how-to-use-sushiswap-farming";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-uniswap-step-by-step.md": {
	id: "defi-yield-how-to-use-uniswap-step-by-step.md";
  slug: "how-to-use-uniswap-a-complete-step-by-step-guide-for-defi-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-how-to-use-yearn-vault-strategies.md": {
	id: "defi-yield-how-to-use-yearn-vault-strategies.md";
  slug: "defi-yield-how-to-use-yearn-vault-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-impermanent-loss-explained-comprehensive-guide-with-examples.md": {
	id: "defi-yield-impermanent-loss-explained-comprehensive-guide-with-examples.md";
  slug: "impermanent-loss-explained-the-complete-guide-to-understanding-and-managing-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-impermanent-loss-explained-simply.md": {
	id: "defi-yield-impermanent-loss-explained-simply.md";
  slug: "defi-yield-impermanent-loss-explained-simply";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-layer-2-defi-opportunities.md": {
	id: "defi-yield-layer-2-defi-opportunities.md";
  slug: "defi-yield-layer-2-defi-opportunities";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-liquidity-pool-mechanics-explained.md": {
	id: "defi-yield-liquidity-pool-mechanics-explained.md";
  slug: "defi-yield-liquidity-pool-mechanics-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-privacy-policy.md": {
	id: "defi-yield-privacy-policy.md";
  slug: "defi-yield-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-real-yield-vs-inflationary-yield-defi.md": {
	id: "defi-yield-real-yield-vs-inflationary-yield-defi.md";
  slug: "defi-yield-real-yield-vs-inflationary-yield-defi";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-terms-of-service.md": {
	id: "defi-yield-terms-of-service.md";
  slug: "defi-yield-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-top-defi-protocols-compared-aave-compound-uniswap-curve.md": {
	id: "defi-yield-top-defi-protocols-compared-aave-compound-uniswap-curve.md";
  slug: "top-defi-protocols-compared-aave-vs-compound-vs-uniswap-vs-curve-your-ultimate-d";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-understanding-defi-governance-tokens.md": {
	id: "defi-yield-understanding-defi-governance-tokens.md";
  slug: "defi-yield-understanding-defi-governance-tokens";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-understanding-total-value-locked-tvl.md": {
	id: "defi-yield-understanding-total-value-locked-tvl.md";
  slug: "defi-yield-understanding-total-value-locked-tvl";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-what-is-defi-explained-simply.md": {
	id: "defi-yield-what-is-defi-explained-simply.md";
  slug: "what-is-defi-explained-simply-a-beginners-guide-to-decentralized-finance";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"defi-yield-yield-farming-impermanent-loss-guide.md": {
	id: "defi-yield-yield-farming-impermanent-loss-guide.md";
  slug: "defi-yield-yield-farming-impermanent-loss-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-about.md": {
	id: "emergency-fund-about.md";
  slug: "emergency-fund-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-automated-savings-strategies.md": {
	id: "emergency-fund-automated-savings-strategies.md";
  slug: "emergency-fund-automated-savings-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-automating-your-set-it-and-forget-it-strategies.md": {
	id: "emergency-fund-automating-your-set-it-and-forget-it-strategies.md";
  slug: "automating-your-emergency-fund-the-set-it-and-forget-it-strategy-for-financial-p";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-benchmarks-by-age-and-income.md": {
	id: "emergency-fund-benchmarks-by-age-and-income.md";
  slug: "emergency-fund-benchmarks-by-age-and-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-banks-for-savings-accounts.md": {
	id: "emergency-fund-best-banks-for-savings-accounts.md";
  slug: "emergency-fund-best-banks-for-savings-accounts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-banks-for-savings.md": {
	id: "emergency-fund-best-banks-for-savings.md";
  slug: "emergency-fund-best-banks-for-savings";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-calculators-and-tools.md": {
	id: "emergency-fund-best-calculators-and-tools.md";
  slug: "emergency-fund-best-calculators-and-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-cd-accounts-for-ladder.md": {
	id: "emergency-fund-best-cd-accounts-for-ladder.md";
  slug: "emergency-fund-best-cd-accounts-for-ladder";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-checking-accounts-for-parking.md": {
	id: "emergency-fund-best-checking-accounts-for-parking.md";
  slug: "emergency-fund-best-checking-accounts-for-parking";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-guide-2025.md": {
	id: "emergency-fund-best-guide-2025.md";
  slug: "emergency-fund-best-guide-2025";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2025.md": {
	id: "emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2025.md";
  slug: "emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2025";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2026.md": {
	id: "emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2026.md";
  slug: "emergency-fund-best-high-yield-savings-accounts-for-emergency-funds-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-hysa-for-emergency-funds-compared-2026.md": {
	id: "emergency-fund-best-hysa-for-emergency-funds-compared-2026.md";
  slug: "emergency-fund-best-hysa-for-emergency-funds-compared-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-money-market-accounts-for-emergency-funds.md": {
	id: "emergency-fund-best-money-market-accounts-for-emergency-funds.md";
  slug: "emergency-fund-best-money-market-accounts-for-emergency-funds";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-places-to-keep-accessible.md": {
	id: "emergency-fund-best-places-to-keep-accessible.md";
  slug: "emergency-fund-best-places-to-keep-accessible";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-savings-apps-for-building.md": {
	id: "emergency-fund-best-savings-apps-for-building.md";
  slug: "emergency-fund-best-savings-apps-for-building";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-savings-strategies-for-irregular-income.md": {
	id: "emergency-fund-best-savings-strategies-for-irregular-income.md";
  slug: "emergency-fund-best-savings-strategies-for-irregular-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-savings-strategies.md": {
	id: "emergency-fund-best-savings-strategies.md";
  slug: "emergency-fund-best-savings-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-treasury-bills-for-yields.md": {
	id: "emergency-fund-best-treasury-bills-for-yields.md";
  slug: "emergency-fund-best-treasury-bills-for-yields";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-best-ways-to-grow-balance.md": {
	id: "emergency-fund-best-ways-to-grow-balance.md";
  slug: "emergency-fund-best-ways-to-grow-balance";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-budget-travel-mistakes-that-could-ruin-your-trip.md": {
	id: "emergency-fund-budget-travel-mistakes-that-could-ruin-your-trip.md";
  slug: "emergency-fund-budget-travel-mistakes-that-could-ruin-your-trip";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-budget-travel-packing-list-the-ultimate-guide.md": {
	id: "emergency-fund-budget-travel-packing-list-the-ultimate-guide.md";
  slug: "emergency-fund-budget-travel-packing-list-the-ultimate-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-calculator-how-much-to-save.md": {
	id: "emergency-fund-calculator-how-much-to-save.md";
  slug: "emergency-fund-calculator-how-much-to-save";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-calculator-how-to-determine-your-exact-savings-target.md": {
	id: "emergency-fund-calculator-how-to-determine-your-exact-savings-target.md";
  slug: "emergency-fund-calculator-how-to-determine-your-exact-savings-target";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-emergency-funds-vs-credit-cards-why-cash-beats-debt-in-a-crisis.md": {
	id: "emergency-fund-emergency-funds-vs-credit-cards-why-cash-beats-debt-in-a-crisis.md";
  slug: "emergency-funds-vs-credit-cards-why-cash-beats-debt-in-a-crisis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-homeowners-unexpected-repairs.md": {
	id: "emergency-fund-for-homeowners-unexpected-repairs.md";
  slug: "emergency-fund-for-homeowners-unexpected-repairs";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-job-loss-protection.md": {
	id: "emergency-fund-for-job-loss-protection.md";
  slug: "emergency-fund-for-job-loss-protection";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-medical-expenses-and-health-crises.md": {
	id: "emergency-fund-for-medical-expenses-and-health-crises.md";
  slug: "emergency-fund-for-medical-expenses-and-health-crises";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-new-parents-guide.md": {
	id: "emergency-fund-for-new-parents-guide.md";
  slug: "emergency-fund-for-new-parents-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-recent-graduates.md": {
	id: "emergency-fund-for-recent-graduates.md";
  slug: "emergency-fund-for-recent-graduates";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-self-employed-and-freelancers.md": {
	id: "emergency-fund-for-self-employed-and-freelancers.md";
  slug: "emergency-fund-for-self-employed-and-freelancers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-for-small-business-owners.md": {
	id: "emergency-fund-for-small-business-owners.md";
  slug: "emergency-fund-for-small-business-owners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-gig-economy-planning-for-freelancers-and-contractors.md": {
	id: "emergency-fund-gig-economy-planning-for-freelancers-and-contractors.md";
  slug: "gig-economy-emergency-fund-planning-the-complete-guide-for-freelancers-and-contr";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-guide-for-beginners.md": {
	id: "emergency-fund-guide-for-beginners.md";
  slug: "emergency-fund-guide-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-guide-for-self-employed-workers.md": {
	id: "emergency-fund-guide-for-self-employed-workers.md";
  slug: "emergency-fund-guide-for-self-employed-workers";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-high-yield-savings-accounts-vs-money-market-for-emergency-funds.md": {
	id: "emergency-fund-high-yield-savings-accounts-vs-money-market-for-emergency-funds.md";
  slug: "high-yield-savings-accounts-vs-money-market-accounts-for-emergency-funds-which-i";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-much-do-i-really-need.md": {
	id: "emergency-fund-how-much-do-i-really-need.md";
  slug: "emergency-fund-how-much-do-i-really-need";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-much-do-you-really-need.md": {
	id: "emergency-fund-how-much-do-you-really-need.md";
  slug: "emergency-fund-how-much-do-you-really-need";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-automate-contributions.md": {
	id: "emergency-fund-how-to-automate-contributions.md";
  slug: "emergency-fund-how-to-automate-contributions";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-automate-your-savings.md": {
	id: "emergency-fund-how-to-automate-your-savings.md";
  slug: "emergency-fund-how-to-automate-your-savings";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-build-3-month-fast.md": {
	id: "emergency-fund-how-to-build-3-month-fast.md";
  slug: "emergency-fund-how-to-build-3-month-fast";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-build-an-from-zero.md": {
	id: "emergency-fund-how-to-build-an-from-zero.md";
  slug: "emergency-fund-how-to-build-an-from-zero";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-build-fast-on-low-income.md": {
	id: "emergency-fund-how-to-build-fast-on-low-income.md";
  slug: "emergency-fund-how-to-build-fast-on-low-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-find-hidden-gem-destinations-on-a-budget.md": {
	id: "emergency-fund-how-to-find-hidden-gem-destinations-on-a-budget.md";
  slug: "emergency-fund-how-to-find-hidden-gem-destinations-on-a-budget";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-handle-during-job-loss.md": {
	id: "emergency-fund-how-to-handle-during-job-loss.md";
  slug: "emergency-fund-how-to-handle-during-job-loss";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-keep-accessible-but-earning-interest.md": {
	id: "emergency-fund-how-to-keep-accessible-but-earning-interest.md";
  slug: "emergency-fund-how-to-keep-accessible-but-earning-interest";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-prioritize-vs-retirement.md": {
	id: "emergency-fund-how-to-prioritize-vs-retirement.md";
  slug: "emergency-fund-how-to-prioritize-vs-retirement";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-prioritize-when-starting-a-new-job.md": {
	id: "emergency-fund-how-to-prioritize-when-starting-a-new-job.md";
  slug: "emergency-fund-how-to-prioritize-when-starting-a-new-job";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-rebuild-after-using-it.md": {
	id: "emergency-fund-how-to-rebuild-after-using-it.md";
  slug: "emergency-fund-how-to-rebuild-after-using-it";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-save-for-while-paying-debt.md": {
	id: "emergency-fund-how-to-save-for-while-paying-debt.md";
  slug: "emergency-fund-how-to-save-for-while-paying-debt";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-save-while-supporting-family.md": {
	id: "emergency-fund-how-to-save-while-supporting-family.md";
  slug: "emergency-fund-how-to-save-while-supporting-family";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-start-an-on-a-minimum-wage-income.md": {
	id: "emergency-fund-how-to-start-an-on-a-minimum-wage-income.md";
  slug: "how-to-start-an-emergency-fund-on-a-minimum-wage-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-start-from-zero.md": {
	id: "emergency-fund-how-to-start-from-zero.md";
  slug: "emergency-fund-how-to-start-from-zero";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-how-to-travel-southeast-asia-on-0-a-day.md": {
	id: "emergency-fund-how-to-travel-southeast-asia-on-0-a-day.md";
  slug: "emergency-fund-how-to-travel-southeast-asia-on-0-a-day";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-investment-options-where-to-park-your-cash.md": {
	id: "emergency-fund-investment-options-where-to-park-your-cash.md";
  slug: "emergency-fund-investment-options-where-to-park-your-cash";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-job-loss-survival-guide-living-on-your-emergency-fund.md": {
	id: "emergency-fund-job-loss-survival-guide-living-on-your-emergency-fund.md";
  slug: "job-loss-survival-guide-living-on-your-emergency-fund";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-medical-emergency-financial-preparation-building-a-healthcare-fund.md": {
	id: "emergency-fund-medical-emergency-financial-preparation-building-a-healthcare-fund.md";
  slug: "medical-emergency-financial-preparation-building-a-healthcare-fund";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-milestones-and-benchmarks.md": {
	id: "emergency-fund-milestones-and-benchmarks.md";
  slug: "emergency-fund-milestones-and-benchmarks";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-myths-that-are-costing-you-money.md": {
	id: "emergency-fund-myths-that-are-costing-you-money.md";
  slug: "emergency-fund-myths-that-are-costing-you-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-natural-disaster-financial-preparedness-protecting-your-money.md": {
	id: "emergency-fund-natural-disaster-financial-preparedness-protecting-your-money.md";
  slug: "natural-disaster-financial-preparedness-protecting-your-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-privacy-policy.md": {
	id: "emergency-fund-privacy-policy.md";
  slug: "emergency-fund-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-rebuilding-your-after-a-major-withdrawal.md": {
	id: "emergency-fund-rebuilding-your-after-a-major-withdrawal.md";
  slug: "rebuilding-your-emergency-fund-after-a-major-withdrawal";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-renters-guide-to-emergency-funds-security-deposits-and-beyond.md": {
	id: "emergency-fund-renters-guide-to-emergency-funds-security-deposits-and-beyond.md";
  slug: "renters-guide-to-emergency-funds-security-deposits-and-beyond";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-seasonal-workers-guide-to-year-round-emergency-savings.md": {
	id: "emergency-fund-seasonal-workers-guide-to-year-round-emergency-savings.md";
  slug: "seasonal-workers-guide-to-year-round-emergency-savings";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-self-employed-emergency-planning-beyond-the-basic-fund.md": {
	id: "emergency-fund-self-employed-emergency-planning-beyond-the-basic-fund.md";
  slug: "self-employed-emergency-planning-beyond-the-basic-fund";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-side-hustles-to-supercharge-your-savings.md": {
	id: "emergency-fund-side-hustles-to-supercharge-your-savings.md";
  slug: "side-hustles-to-supercharge-your-emergency-fund-savings";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-size-by-age-and-lifestyle-a-complete-breakdown.md": {
	id: "emergency-fund-size-by-age-and-lifestyle-a-complete-breakdown.md";
  slug: "emergency-fund-size-by-age-and-lifestyle-a-complete-breakdown";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-strategies-for-couples-joint-vs-separate-savings.md": {
	id: "emergency-fund-strategies-for-couples-joint-vs-separate-savings.md";
  slug: "emergency-fund-strategies-for-couples-joint-vs-separate-savings";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-teaching-kids-about-emergency-funds-and-financial-safety-nets.md": {
	id: "emergency-fund-teaching-kids-about-emergency-funds-and-financial-safety-nets.md";
  slug: "teaching-kids-about-emergency-funds-and-financial-safety-nets";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-terms-of-service.md": {
	id: "emergency-fund-terms-of-service.md";
  slug: "emergency-fund-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-top-mistakes-to-avoid.md": {
	id: "emergency-fund-top-mistakes-to-avoid.md";
  slug: "emergency-fund-top-mistakes-to-avoid";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-vs-credit-line-which-is-better.md": {
	id: "emergency-fund-vs-credit-line-which-is-better.md";
  slug: "emergency-fund-vs-credit-line-which-is-better";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-vs-insurance-understanding-when-to-use-each.md": {
	id: "emergency-fund-vs-insurance-understanding-when-to-use-each.md";
  slug: "emergency-fund-vs-insurance-understanding-when-to-use-each";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-vs-investing-which-comes-first.md": {
	id: "emergency-fund-vs-investing-which-comes-first.md";
  slug: "emergency-fund-vs-investing-which-comes-first";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-vs-paying-off-debt-first.md": {
	id: "emergency-fund-vs-paying-off-debt-first.md";
  slug: "emergency-fund-vs-paying-off-debt-first";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"emergency-fund-vs-savings-account.md": {
	id: "emergency-fund-vs-savings-account.md";
  slug: "emergency-fund-vs-savings-account";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-dex-for-memecoin-trading.md": {
	id: "memecoin-trading-best-dex-for-memecoin-trading.md";
  slug: "memecoin-trading-best-dex-for-memecoin-trading";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-hardware-wallets-for-memecoins.md": {
	id: "memecoin-trading-best-hardware-wallets-for-memecoins.md";
  slug: "memecoin-trading-best-hardware-wallets-for-memecoins";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-memecoin-communities-to-join.md": {
	id: "memecoin-trading-best-memecoin-communities-to-join.md";
  slug: "memecoin-trading-best-memecoin-communities-to-join";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-memecoin-trackers-and-tools.md": {
	id: "memecoin-trading-best-memecoin-trackers-and-tools.md";
  slug: "memecoin-trading-best-memecoin-trackers-and-tools";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-memecoins-to-buy-2026.md": {
	id: "memecoin-trading-best-memecoins-to-buy-2026.md";
  slug: "memecoin-trading-best-memecoins-to-buy-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-technical-indicators-for-memecoins.md": {
	id: "memecoin-trading-best-technical-indicators-for-memecoins.md";
  slug: "memecoin-trading-best-technical-indicators-for-memecoins";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-time-to-buy-memecoins-2026.md": {
	id: "memecoin-trading-best-time-to-buy-memecoins-2026.md";
  slug: "memecoin-trading-best-time-to-buy-memecoins-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-time-to-enter-memecoin-projects.md": {
	id: "memecoin-trading-best-time-to-enter-memecoin-projects.md";
  slug: "memecoin-trading-best-time-to-enter-memecoin-projects";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-best-wallets-for-memecoin-storage.md": {
	id: "memecoin-trading-best-wallets-for-memecoin-storage.md";
  slug: "memecoin-trading-best-wallets-for-memecoin-storage";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-dogecoin-alternatives-2026.md": {
	id: "memecoin-trading-dogecoin-alternatives-2026.md";
  slug: "memecoin-trading-dogecoin-alternatives-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-analyze-memecoin-social-media-hype.md": {
	id: "memecoin-trading-how-to-analyze-memecoin-social-media-hype.md";
  slug: "memecoin-trading-how-to-analyze-memecoin-social-media-hype";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-analyze-memecoin-tokenomics.md": {
	id: "memecoin-trading-how-to-analyze-memecoin-tokenomics.md";
  slug: "memecoin-trading-how-to-analyze-memecoin-tokenomics";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-avoid-memecoin-rug-pulls.md": {
	id: "memecoin-trading-how-to-avoid-memecoin-rug-pulls.md";
  slug: "memecoin-trading-how-to-avoid-memecoin-rug-pulls";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-bridge-sol-for-memecoin-purchases.md": {
	id: "memecoin-trading-how-to-bridge-sol-for-memecoin-purchases.md";
  slug: "memecoin-trading-how-to-bridge-sol-for-memecoin-purchases";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-build-a-diversified-memecoin-portfolio.md": {
	id: "memecoin-trading-how-to-build-a-diversified-memecoin-portfolio.md";
  slug: "memecoin-trading-how-to-build-a-diversified-memecoin-portfolio";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-buy-memecoins-on-raydium.md": {
	id: "memecoin-trading-how-to-buy-memecoins-on-raydium.md";
  slug: "memecoin-trading-how-to-buy-memecoins-on-raydium";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-create-a-memecoin-strategy-plan.md": {
	id: "memecoin-trading-how-to-create-a-memecoin-strategy-plan.md";
  slug: "memecoin-trading-how-to-create-a-memecoin-strategy-plan";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-find-new-memecoins-early.md": {
	id: "memecoin-trading-how-to-find-new-memecoins-early.md";
  slug: "memecoin-trading-how-to-find-new-memecoins-early";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-participate-in-memecoin-presales.md": {
	id: "memecoin-trading-how-to-participate-in-memecoin-presales.md";
  slug: "memecoin-trading-how-to-participate-in-memecoin-presales";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-read-memecoin-charts-like-a-pro.md": {
	id: "memecoin-trading-how-to-read-memecoin-charts-like-a-pro.md";
  slug: "memecoin-trading-how-to-read-memecoin-charts-like-a-pro";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-read-memecoin-tokenomics.md": {
	id: "memecoin-trading-how-to-read-memecoin-tokenomics.md";
  slug: "memecoin-trading-how-to-read-memecoin-tokenomics";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-research-new-memecoin-projects.md": {
	id: "memecoin-trading-how-to-research-new-memecoin-projects.md";
  slug: "memecoin-trading-how-to-research-new-memecoin-projects";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-set-up-dashboard.md": {
	id: "memecoin-trading-how-to-set-up-dashboard.md";
  slug: "memecoin-trading-how-to-set-up-dashboard";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-spot-emerging-memecoin-trends.md": {
	id: "memecoin-trading-how-to-spot-emerging-memecoin-trends.md";
  slug: "memecoin-trading-how-to-spot-emerging-memecoin-trends";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-how-to-trade-memecoins-for-beginners.md": {
	id: "memecoin-trading-how-to-trade-memecoins-for-beginners.md";
  slug: "memecoin-trading-how-to-trade-memecoins-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-airdrop-farming-strategies.md": {
	id: "memecoin-trading-memecoin-airdrop-farming-strategies.md";
  slug: "memecoin-trading-memecoin-airdrop-farming-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-community-building-techniques.md": {
	id: "memecoin-trading-memecoin-community-building-techniques.md";
  slug: "memecoin-trading-memecoin-community-building-techniques";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-exchange-listing-strategies.md": {
	id: "memecoin-trading-memecoin-exchange-listing-strategies.md";
  slug: "memecoin-trading-memecoin-exchange-listing-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-fundamental-analysis-guide.md": {
	id: "memecoin-trading-memecoin-fundamental-analysis-guide.md";
  slug: "memecoin-trading-memecoin-fundamental-analysis-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-leverage-trading-explained.md": {
	id: "memecoin-trading-memecoin-leverage-trading-explained.md";
  slug: "memecoin-trading-memecoin-leverage-trading-explained";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-liquidity-pool-farming-guide.md": {
	id: "memecoin-trading-memecoin-liquidity-pool-farming-guide.md";
  slug: "memecoin-trading-memecoin-liquidity-pool-farming-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-liquidity-pool-strategies.md": {
	id: "memecoin-trading-memecoin-liquidity-pool-strategies.md";
  slug: "memecoin-trading-memecoin-liquidity-pool-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-market-cycle-analysis.md": {
	id: "memecoin-trading-memecoin-market-cycle-analysis.md";
  slug: "memecoin-trading-memecoin-market-cycle-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-market-sentiment-indicators.md": {
	id: "memecoin-trading-memecoin-market-sentiment-indicators.md";
  slug: "memecoin-trading-memecoin-market-sentiment-indicators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-portfolio-rebalancing-strategies.md": {
	id: "memecoin-trading-memecoin-portfolio-rebalancing-strategies.md";
  slug: "memecoin-trading-memecoin-portfolio-rebalancing-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-portfolio-strategy-2026.md": {
	id: "memecoin-trading-memecoin-portfolio-strategy-2026.md";
  slug: "memecoin-trading-memecoin-portfolio-strategy-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-project-fundamentals-checklist.md": {
	id: "memecoin-trading-memecoin-project-fundamentals-checklist.md";
  slug: "memecoin-trading-memecoin-project-fundamentals-checklist";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-project-team-analysis.md": {
	id: "memecoin-trading-memecoin-project-team-analysis.md";
  slug: "memecoin-trading-memecoin-project-team-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-project-token-distribution-analysis.md": {
	id: "memecoin-trading-memecoin-project-token-distribution-analysis.md";
  slug: "memecoin-trading-memecoin-project-token-distribution-analysis";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-regulatory-landscape-2026.md": {
	id: "memecoin-trading-memecoin-regulatory-landscape-2026.md";
  slug: "memecoin-trading-memecoin-regulatory-landscape-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-risk-management-strategies.md": {
	id: "memecoin-trading-memecoin-risk-management-strategies.md";
  slug: "memecoin-trading-memecoin-risk-management-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-tax-implications-2026.md": {
	id: "memecoin-trading-memecoin-tax-implications-2026.md";
  slug: "memecoin-trading-memecoin-tax-implications-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-versus-shitcoin-identification.md": {
	id: "memecoin-trading-memecoin-versus-shitcoin-identification.md";
  slug: "memecoin-trading-memecoin-versus-shitcoin-identification";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-volatility-trading-strategies.md": {
	id: "memecoin-trading-memecoin-volatility-trading-strategies.md";
  slug: "memecoin-trading-memecoin-volatility-trading-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-vs-altcoin-comparison.md": {
	id: "memecoin-trading-memecoin-vs-altcoin-comparison.md";
  slug: "memecoin-trading-memecoin-vs-altcoin-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-vs-bitcoin-comparison.md": {
	id: "memecoin-trading-memecoin-vs-bitcoin-comparison.md";
  slug: "memecoin-trading-memecoin-vs-bitcoin-comparison";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-memecoin-vs-traditional-crypto-volatility.md": {
	id: "memecoin-trading-memecoin-vs-traditional-crypto-volatility.md";
  slug: "memecoin-trading-memecoin-vs-traditional-crypto-volatility";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-risk-management-techniques.md": {
	id: "memecoin-trading-risk-management-techniques.md";
  slug: "memecoin-trading-risk-management-techniques";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-safest-memecoin-investment-strategies.md": {
	id: "memecoin-trading-safest-memecoin-investment-strategies.md";
  slug: "memecoin-trading-safest-memecoin-investment-strategies";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-signals-and-indicators.md": {
	id: "memecoin-trading-signals-and-indicators.md";
  slug: "memecoin-trading-signals-and-indicators";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-solana-memecoin-ecosystem-guide.md": {
	id: "memecoin-trading-solana-memecoin-ecosystem-guide.md";
  slug: "memecoin-trading-solana-memecoin-ecosystem-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-solana-memecoins-to-watch.md": {
	id: "memecoin-trading-solana-memecoins-to-watch.md";
  slug: "memecoin-trading-solana-memecoins-to-watch";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-top-performing-memecoins-2026.md": {
	id: "memecoin-trading-top-performing-memecoins-2026.md";
  slug: "memecoin-trading-top-performing-memecoins-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"memecoin-trading-when-to-sell-memecoin-profits.md": {
	id: "memecoin-trading-when-to-sell-memecoin-profits.md";
  slug: "memecoin-trading-when-to-sell-memecoin-profits";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-50-30-20-rule-the-ultimate-budgeting-framework.md": {
	id: "personal-finance-50-30-20-rule-the-ultimate-budgeting-framework.md";
  slug: "personal-finance-50-30-20-rule-the-ultimate-budgeting-framework";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-about.md": {
	id: "personal-finance-about.md";
  slug: "personal-finance-about";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-bank-accounts-for-teens.md": {
	id: "personal-finance-best-bank-accounts-for-teens.md";
  slug: "personal-finance-best-bank-accounts-for-teens";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-books.md": {
	id: "personal-finance-best-books.md";
  slug: "personal-finance-best-books";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-budget-travel-destinations-under-500.md": {
	id: "personal-finance-best-budget-travel-destinations-under-500.md";
  slug: "personal-finance-best-budget-travel-destinations-under-500";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-budgeting-apps-2026.md": {
	id: "personal-finance-best-budgeting-apps-2026.md";
  slug: "personal-finance-best-budgeting-apps-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-budgeting-apps-and-tools-compared.md": {
	id: "personal-finance-best-budgeting-apps-and-tools-compared.md";
  slug: "personal-finance-best-budgeting-apps-and-tools-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-budgeting-methods-compared.md": {
	id: "personal-finance-best-budgeting-methods-compared.md";
  slug: "personal-finance-best-budgeting-methods-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-cashback-credit-cards-2026.md": {
	id: "personal-finance-best-cashback-credit-cards-2026.md";
  slug: "personal-finance-best-cashback-credit-cards-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-checking-accounts-2026.md": {
	id: "personal-finance-best-checking-accounts-2026.md";
  slug: "personal-finance-best-checking-accounts-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-credit-monitoring-services.md": {
	id: "personal-finance-best-credit-monitoring-services.md";
  slug: "personal-finance-best-credit-monitoring-services";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-debt-payoff-methods-snowball-vs-avalanche.md": {
	id: "personal-finance-best-debt-payoff-methods-snowball-vs-avalanche.md";
  slug: "personal-finance-best-debt-payoff-methods-snowball-vs-avalanche";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-financial-podcasts-to-follow.md": {
	id: "personal-finance-best-financial-podcasts-to-follow.md";
  slug: "personal-finance-best-financial-podcasts-to-follow";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-high-yield-savings-accounts-compared.md": {
	id: "personal-finance-best-high-yield-savings-accounts-compared.md";
  slug: "personal-finance-best-high-yield-savings-accounts-compared";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-high-yield-savings-accounts.md": {
	id: "personal-finance-best-high-yield-savings-accounts.md";
  slug: "personal-finance-best-high-yield-savings-accounts";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-identity-theft-protection.md": {
	id: "personal-finance-best-identity-theft-protection.md";
  slug: "personal-finance-best-identity-theft-protection";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-index-funds-for-beginners.md": {
	id: "personal-finance-best-index-funds-for-beginners.md";
  slug: "personal-finance-best-index-funds-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-investment-apps-for-beginners.md": {
	id: "personal-finance-best-investment-apps-for-beginners.md";
  slug: "personal-finance-best-investment-apps-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-money-management-for-couples.md": {
	id: "personal-finance-best-money-management-for-couples.md";
  slug: "personal-finance-best-money-management-for-couples";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-money-saving-tips-2026.md": {
	id: "personal-finance-best-money-saving-tips-2026.md";
  slug: "personal-finance-best-money-saving-tips-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-savings-bonds-for-beginners.md": {
	id: "personal-finance-best-savings-bonds-for-beginners.md";
  slug: "personal-finance-best-savings-bonds-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-side-hustles-for-passive-income.md": {
	id: "personal-finance-best-side-hustles-for-passive-income.md";
  slug: "personal-finance-best-side-hustles-for-passive-income";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-best-ways-to-invest-1000-dollars.md": {
	id: "personal-finance-best-ways-to-invest-1000-dollars.md";
  slug: "personal-finance-best-ways-to-invest-1000-dollars";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-emergency-fund-how-much-to-save.md": {
	id: "personal-finance-emergency-fund-how-much-to-save.md";
  slug: "personal-finance-emergency-fund-how-much-to-save";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-emergency-fund-how-much-you-really-need.md": {
	id: "personal-finance-emergency-fund-how-much-you-really-need.md";
  slug: "personal-finance-emergency-fund-how-much-you-really-need";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-faq-20-questions-answered.md": {
	id: "personal-finance-faq-20-questions-answered.md";
  slug: "personal-finance-faq-20-questions-answered";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-financial-independence-retire-early-fire.md": {
	id: "personal-finance-financial-independence-retire-early-fire.md";
  slug: "personal-finance-financial-independence-retire-early-fire";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-high-yield-savings-account-strategies-2026.md": {
	id: "personal-finance-high-yield-savings-account-strategies-2026.md";
  slug: "personal-finance-high-yield-savings-account-strategies-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-automate-your-finances.md": {
	id: "personal-finance-how-to-automate-your-finances.md";
  slug: "personal-finance-how-to-automate-your-finances";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-build-an-emergency-fund-fast.md": {
	id: "personal-finance-how-to-build-an-emergency-fund-fast.md";
  slug: "personal-finance-how-to-build-an-emergency-fund-fast";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-build-credit-from-scratch-step-by-step.md": {
	id: "personal-finance-how-to-build-credit-from-scratch-step-by-step.md";
  slug: "personal-finance-how-to-build-credit-from-scratch-step-by-step";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-build-multiple-income-streams.md": {
	id: "personal-finance-how-to-build-multiple-income-streams.md";
  slug: "personal-finance-how-to-build-multiple-income-streams";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-create-a-budget-that-actually-works-in-2026.md": {
	id: "personal-finance-how-to-create-a-budget-that-actually-works-in-2026.md";
  slug: "personal-finance-how-to-create-a-budget-that-actually-works-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-create-a-budget-that-works.md": {
	id: "personal-finance-how-to-create-a-budget-that-works.md";
  slug: "personal-finance-how-to-create-a-budget-that-works";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-create-a-financial-plan.md": {
	id: "personal-finance-how-to-create-a-financial-plan.md";
  slug: "personal-finance-how-to-create-a-financial-plan";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-dispute-credit-report-errors.md": {
	id: "personal-finance-how-to-dispute-credit-report-errors.md";
  slug: "personal-finance-how-to-dispute-credit-report-errors";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-handle-debt-collectors.md": {
	id: "personal-finance-how-to-handle-debt-collectors.md";
  slug: "personal-finance-how-to-handle-debt-collectors";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-improve-credit-score-fast.md": {
	id: "personal-finance-how-to-improve-credit-score-fast.md";
  slug: "personal-finance-how-to-improve-credit-score-fast";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-negotiate-a-higher-salary-complete-guide.md": {
	id: "personal-finance-how-to-negotiate-a-higher-salary-complete-guide.md";
  slug: "personal-finance-how-to-negotiate-a-higher-salary-complete-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-negotiate-bills-and-save-thousands.md": {
	id: "personal-finance-how-to-negotiate-bills-and-save-thousands.md";
  slug: "personal-finance-how-to-negotiate-bills-and-save-thousands";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-negotiate-bills-down.md": {
	id: "personal-finance-how-to-negotiate-bills-down.md";
  slug: "personal-finance-how-to-negotiate-bills-down";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-negotiate-salary-effectively.md": {
	id: "personal-finance-how-to-negotiate-salary-effectively.md";
  slug: "personal-finance-how-to-negotiate-salary-effectively";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-pay-off-credit-card-debt-fast.md": {
	id: "personal-finance-how-to-pay-off-credit-card-debt-fast.md";
  slug: "personal-finance-how-to-pay-off-credit-card-debt-fast";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-pay-off-debt-fast-complete-strategy-guide.md": {
	id: "personal-finance-how-to-pay-off-debt-fast-complete-strategy-guide.md";
  slug: "personal-finance-how-to-pay-off-debt-fast-complete-strategy-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-read-your-credit-report.md": {
	id: "personal-finance-how-to-read-your-credit-report.md";
  slug: "personal-finance-how-to-read-your-credit-report";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-reduce-monthly-expenses.md": {
	id: "personal-finance-how-to-reduce-monthly-expenses.md";
  slug: "personal-finance-how-to-reduce-monthly-expenses";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-refinance-student-loans.md": {
	id: "personal-finance-how-to-refinance-student-loans.md";
  slug: "personal-finance-how-to-refinance-student-loans";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-save-money-every-month.md": {
	id: "personal-finance-how-to-save-money-every-month.md";
  slug: "personal-finance-how-to-save-money-every-month";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-save-money-on-groceries-without-coupons.md": {
	id: "personal-finance-how-to-save-money-on-groceries-without-coupons.md";
  slug: "personal-finance-how-to-save-money-on-groceries-without-coupons";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-start-a-sole-proprietorship.md": {
	id: "personal-finance-how-to-start-a-sole-proprietorship.md";
  slug: "personal-finance-how-to-start-a-sole-proprietorship";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-start-investing-with-100-dollars.md": {
	id: "personal-finance-how-to-start-investing-with-100-dollars.md";
  slug: "personal-finance-how-to-start-investing-with-100-dollars";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-stop-living-paycheck-to-paycheck.md": {
	id: "personal-finance-how-to-stop-living-paycheck-to-paycheck.md";
  slug: "personal-finance-how-to-stop-living-paycheck-to-paycheck";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-teach-kids-about-money.md": {
	id: "personal-finance-how-to-teach-kids-about-money.md";
  slug: "personal-finance-how-to-teach-kids-about-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-how-to-teach-teenagers-about-credit.md": {
	id: "personal-finance-how-to-teach-teenagers-about-credit.md";
  slug: "personal-finance-how-to-teach-teenagers-about-credit";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-index-fund-investing-the-lazy-path-to-wealth.md": {
	id: "personal-finance-index-fund-investing-the-lazy-path-to-wealth.md";
  slug: "personal-finance-index-fund-investing-the-lazy-path-to-wealth";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-investing-for-beginners-guide.md": {
	id: "personal-finance-investing-for-beginners-guide.md";
  slug: "personal-finance-investing-for-beginners-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-money-mistakes-to-avoid-in-your-20s.md": {
	id: "personal-finance-money-mistakes-to-avoid-in-your-20s.md";
  slug: "personal-finance-money-mistakes-to-avoid-in-your-20s";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-privacy-policy.md": {
	id: "personal-finance-privacy-policy.md";
  slug: "personal-finance-privacy-policy";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-real-estate-investing-for-beginners.md": {
	id: "personal-finance-real-estate-investing-for-beginners.md";
  slug: "personal-finance-real-estate-investing-for-beginners";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-real-estate-vs-stocks-where-to-invest-your-money.md": {
	id: "personal-finance-real-estate-vs-stocks-where-to-invest-your-money.md";
  slug: "personal-finance-real-estate-vs-stocks-where-to-invest-your-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-retirement-planning-guide-for-millennials-and-gen-z.md": {
	id: "personal-finance-retirement-planning-guide-for-millennials-and-gen-z.md";
  slug: "personal-finance-retirement-planning-guide-for-millennials-and-gen-z";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-side-hustle-ideas-that-actually-pay-well-in-2026.md": {
	id: "personal-finance-side-hustle-ideas-that-actually-pay-well-in-2026.md";
  slug: "personal-finance-side-hustle-ideas-that-actually-pay-well-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-side-hustle-ideas-to-make-extra-money.md": {
	id: "personal-finance-side-hustle-ideas-to-make-extra-money.md";
  slug: "personal-finance-side-hustle-ideas-to-make-extra-money";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-side-hustle-income-tax-guide.md": {
	id: "personal-finance-side-hustle-income-tax-guide.md";
  slug: "personal-finance-side-hustle-income-tax-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-tax-loss-harvesting-complete-strategy-guide.md": {
	id: "personal-finance-tax-loss-harvesting-complete-strategy-guide.md";
  slug: "personal-finance-tax-loss-harvesting-complete-strategy-guide";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-tax-saving-strategies-for-individuals.md": {
	id: "personal-finance-tax-saving-strategies-for-individuals.md";
  slug: "personal-finance-tax-saving-strategies-for-individuals";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-terms-of-service.md": {
	id: "personal-finance-terms-of-service.md";
  slug: "personal-finance-terms-of-service";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-top-10-investing-apps-for-beginners-in-2026.md": {
	id: "personal-finance-top-10-investing-apps-for-beginners-in-2026.md";
  slug: "personal-finance-top-10-investing-apps-for-beginners-in-2026";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-understanding-401k-and-retirement.md": {
	id: "personal-finance-understanding-401k-and-retirement.md";
  slug: "personal-finance-understanding-401k-and-retirement";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
"personal-finance-understanding-compound-interest.md": {
	id: "personal-finance-understanding-compound-interest.md";
  slug: "personal-finance-understanding-compound-interest";
  body: string;
  collection: "articles";
  data: any
} & { render(): Render[".md"] };
};

	};

	type DataEntryMap = {
		
	};

	type AnyEntryMap = ContentEntryMap & DataEntryMap;

	export type ContentConfig = never;
}
