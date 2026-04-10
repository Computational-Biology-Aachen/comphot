<script lang="ts">
	interface ParamRow {
		label: string;
		newVal: string | number;
		oldVal?: string | number;
	}

	interface Props {
		rows: ParamRow[];
		showOld?: boolean;
		newLabel?: string;
		oldLabel?: string;
	}

	let { rows, showOld = false, newLabel = 'New', oldLabel = 'Old' }: Props = $props();
</script>

<div class="param-table-wrap">
	<table class="param-table">
		<thead>
			<tr>
				<th>Parameter</th>
				<th>{newLabel}</th>
				{#if showOld}
					<th>{oldLabel}</th>
				{/if}
			</tr>
		</thead>
		<tbody>
			{#each rows as row}
				<tr>
					<td>{row.label}</td>
					<td class="val">{row.newVal}</td>
					{#if showOld}
						<td class="val">{row.oldVal ?? '—'}</td>
					{/if}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.param-table-wrap {
		overflow-x: auto;
	}

	.param-table {
		border-collapse: collapse;
		font-size: 0.85rem;
		width: 100%;
	}

	th,
	td {
		padding: 0.35rem 0.75rem;
		text-align: left;
		border-bottom: 1px solid var(--color-border);
	}

	th {
		font-weight: 600;
		background: var(--color-surface);
		white-space: nowrap;
	}

	.val {
		font-variant-numeric: tabular-nums;
		font-family: var(--font-mono);
		font-size: 0.8rem;
	}
</style>
