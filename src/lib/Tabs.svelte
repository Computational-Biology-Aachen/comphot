<script lang="ts">
  import { ButtonTab } from "@computational-biology-aachen/design";
  import type { Snippet } from "svelte";

  let {
    tabs,
    children,
  }: {
    tabs: { key: string; label: string }[];
    children: Snippet<[string]>;
  } = $props();

  let activeKey = $state("");

  $effect(() => {
    if (!tabs.some((t) => t.key === activeKey)) {
      activeKey = tabs[0]?.key ?? "";
    }
  });
</script>

<div class="tab-bar" role="tablist">
  {#each tabs as tab (tab.key)}
    <ButtonTab
      selected={activeKey === tab.key}
      onclick={() => (activeKey = tab.key)}
    >
      {tab.label}
    </ButtonTab>
  {/each}
</div>

<div class="tab-content">
  {@render children(activeKey)}
</div>

<style>
  .tab-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: var(--space-4, 16px);
  }

  .tab-content {
    min-height: 4rem;
  }
</style>
