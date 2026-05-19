<script lang="ts">
  import { base } from "$app/paths";
  import { page } from "$app/state";
  import favicon from "$lib/assets/cpbl-favicon.svg";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import * as config from "$lib/config";
  import * as m from "$lib/paraglide/messages";
  import { locales, localizeHref } from "$lib/paraglide/runtime";
  import { Navbar, NavGH } from "@computational-biology-aachen/design";
  import "../app.css";

  let { children } = $props();

  // Get the route path without base prefix for localizeHref
  function routePath() {
    const routeId = page.route.id ?? "/";
    return routeId;
  }
</script>

<svelte:head>
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
  <title>{m.str_headline_main()} | ComPhot</title>
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
    <a
      href="{base}/"
      class="brand">ComPhot</a
    >
  {/snippet}
  <NavGH />
</Navbar>
<Sidebar />
{@render children()}

<style>
  .brand {
    color: var(--color-primary);
    font-weight: 600;
    font-size: 1.2rem;
    letter-spacing: -0.01em;
    text-decoration: none;
  }
</style>
