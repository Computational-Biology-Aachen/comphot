<script lang="ts">
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import type { Res } from "$lib/stores/workerStore";
  import type { PhaseRegion } from "../../../../packages/design/src/lib/SimChart.svelte";
  import SimChart from "../../../../packages/design/src/lib/SimChart.svelte";
  import ParameterTable from "../../../../packages/design/src/lib/TableParameter.svelte";

  interface ParamRow {
    label: string;
    newVal: string | number;
    oldVal?: string | number;
  }

  interface Props {
    currentResult: Res;
    previousResult: Res | null;
    showOld: boolean;
    phases: PhaseRegion[];
    totalTime: number;
    paramRows: ParamRow[];
    showOldParams: boolean;
  }

  let {
    currentResult,
    previousResult,
    showOld,
    phases,
    totalTime,
    paramRows,
    showOldParams,
  }: Props = $props();

  const prev = $derived(showOld && previousResult ? previousResult : null);
</script>

<div class="charts-section">
  <div
    class="charts-grid"
    class:three-cols={audienceStore.audience === "4bio"}
  >
    <div class="chart-card">
      <p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
      <SimChart
        xNew={currentResult.time}
        yNew={currentResult.fluo}
        xOld={prev?.time ?? []}
        yOld={prev?.fluo ?? []}
        phases={phases}
        yLabel={ta(m.bio_fluo(), m.math_fluo())}
        showLine={true}
        totalTime={totalTime}
      />
    </div>

    {#if audienceStore.audience === "4bio"}
      <div class="chart-card">
        <p class="chart-label">{m.axis_npq()}</p>
        <SimChart
          xNew={currentResult.npqTime}
          yNew={currentResult.npq}
          xOld={prev?.npqTime ?? []}
          yOld={prev?.npq ?? []}
          phases={phases}
          yLabel={m.axis_npq()}
          showLine={false}
          totalTime={totalTime}
        />
      </div>

      <div class="chart-card">
        <p class="chart-label">{m.axis_phipsii()}</p>
        <SimChart
          xNew={currentResult.npqTime}
          yNew={currentResult.phiPsii}
          xOld={prev?.npqTime ?? []}
          yOld={prev?.phiPsii ?? []}
          phases={phases}
          yLabel={m.axis_phipsii()}
          showLine={false}
          totalTime={totalTime}
        />
      </div>
    {/if}
  </div>

  {#if paramRows.length > 0}
    <div class="param-table-wrap">
      <ParameterTable
        rows={paramRows}
        showOld={showOldParams}
        newLabel={m.new_label()}
        oldLabel={m.old_label()}
      />
    </div>
  {/if}
</div>
