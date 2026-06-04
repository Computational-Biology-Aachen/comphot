<script lang="ts">
  import { base } from "$app/paths";
  import { page } from "$app/state";
  import favicon from "$lib/assets/cpbl-favicon.svg";
  import * as config from "$lib/config";
  import {
    getLocale,
    locales,
    localizeHref,
    setLocale,
  } from "$lib/paraglide/runtime";
  import { audienceStore, type Audience } from "$lib/stores/audience.svelte";
  import {
    ButtonMenu,
    ButtonMenuItem,
    CollapseToBurger,
    Icon,
    Navbar,
    NavGH,
    NavItem,
  } from "@computational-biology-aachen/design";
  import type { Snippet } from "svelte";
  import "../app.css";

  type Lang = "en" | "de" | "fr";

  let {
    children,
  }: {
    children: Snippet;
  } = $props();

  const locChoices: { code: Lang; label: string }[] = [
    { code: "en", label: "en" },
    { code: "de", label: "de" },
    { code: "fr", label: "fr" },
  ];
  const audChoices: { code: Audience; label: string }[] = [
    { code: "4bio", label: "4bio" },
    { code: "4math", label: "4math" },
  ];

  let currentLocale = $state(getLocale());
  function switchLocale(code: Lang) {
    setLocale(code);
    currentLocale = getLocale();
  }

  // Get the route path without base prefix for localizeHref
  function routePath() {
    const routeId = page.route.id ?? "/";
    return routeId;
  }
</script>

<svelte:head>
  <title>ComPhot</title>
  <meta
    name="description"
    content={config.description}
  />
  <meta
    property="og:title"
    content={config.title}
  />
  <meta
    property="og:description"
    content={config.description}
  />
  <meta
    property="og:url"
    content={config.url}
  />
  <meta
    property="og:type"
    content="website"
  />
  <meta
    name="twitter:card"
    content="summary"
  />
  <link
    rel="icon"
    href={favicon}
  />
  <!-- Alternate locale links for crawlers -->
  {#each locales as locale (locale)}
    <link
      rel="alternate"
      hreflang={locale}
      href="{base}{localizeHref(routePath(), { locale })}"
    />
  {/each}
  <meta
    property="og:type"
    content="website"
  />
  <meta
    name="twitter:card"
    content="summary"
  />
</svelte:head>

<!-- Hidden locale links for Paraglide's prerender crawler -->
<div style="display:none">
  {#each locales as locale (locale)}
    <a href="{base}{localizeHref(routePath(), { locale })}">{locale}</a>
  {/each}
</div>

<Navbar>
  {#snippet brand()}
    <div class="brand">
      <span>ComPhot</span>
    </div>
  {/snippet}
  <CollapseToBurger collapseAt="1200px">
    <NavItem href="{base}/">Home</NavItem>
    <NavItem href="{base}/photosynthesis">Photosynthesis</NavItem>
    <NavItem href="{base}/method">Method</NavItem>
    <NavItem href="{base}/model">Model</NavItem>
    <NavItem href="{base}/experiments">Experiments</NavItem>
    <NavItem href="{base}/plant-memory">Plant Memory</NavItem>
    <NavItem href="{base}/conclusion">Conclusion</NavItem>
    <NavItem href="{base}/contact">Contact</NavItem>
  </CollapseToBurger>
  <ButtonMenu>
    {#snippet label()}
      <Icon>group</Icon>
    {/snippet}
    {#each audChoices as { code, label } (code)}
      <ButtonMenuItem
        active={audienceStore.audience === code}
        onclick={() => audienceStore.setAudience(code)}
      >
        {label}
      </ButtonMenuItem>
    {/each}
  </ButtonMenu>
  <ButtonMenu>
    {#snippet label()}
      <Icon>language</Icon>
    {/snippet}
    {#each locChoices as { code, label } (code)}
      <ButtonMenuItem
        active={currentLocale === code}
        onclick={() => switchLocale(code)}
      >
        {label}
      </ButtonMenuItem>
    {/each}
  </ButtonMenu>

  <NavGH href="https://github.com/Computational-Biology-Aachen/comphot" />
</Navbar>

{@render children()}

<style>
  .brand {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-primary);
    font-weight: 600;
  }
</style>
