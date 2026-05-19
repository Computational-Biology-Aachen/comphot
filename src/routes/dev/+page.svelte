<script lang="ts">
	import CompareCheckbox from '$lib/components/simulation/CompareCheckbox.svelte';
	import { LineChart } from '@computational-biology-aachen/design';
	import ParameterTable from '$lib/components/simulation/ParameterTable.svelte';
	import { Button } from '@computational-biology-aachen/design';
	import type { PhaseRegion } from '$lib/components/simulation/SimChart.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { buildPamProtocol } from '$lib/simulations/pam';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { LOG_STEPS, SimState } from '$lib/stores/simState.svelte';

	const sim = new SimState();
	sim.setup();

	// Slider state
	let lightIntensity = $state(100);
	let totalMinutes = $state(1);
	let pulseInterval = $state(85);
	let darkLength = $state(30);
	let saturatingPulse = $state(5000);
	let compareWithLast = $state(true);

	// Logspace sliders
	let activationIdx = $state(10); // LOG_STEPS[10] = 100
	let deactivationIdx = $state(10);
	const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
	const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);
	const totalTime = $derived(totalMinutes * 60);

	function runSimulation() {
		const protocol = buildPamProtocol({
			lightIntensity,
			saturatingPulse,
			totalMinutes,
			darkLength,
			pulseInterval
		});
		const kDeepoxV = 0.0024 * (activationMultiplier / 100);
		const kEpoxZ = 0.00024 * (deactivationMultiplier / 100);
		sim.run(protocol, { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ }, [
			kDeepoxV,
			kEpoxZ
		]);
	}

	// Phase background regions
	const phases = $derived.by<PhaseRegion[]>(() => {
		const dl = darkLength;
		const maxT = totalMinutes * 60;
		return [
			{ start: 0, end: dl, color: 'rgba(28, 91, 199, 0.18)' },
			{ start: dl, end: maxT, color: 'rgba(207, 109, 12, 0.18)' }
		];
	});

	// Derived display
	const showOld = $derived(compareWithLast && sim.previousResult !== null);

	const paramRows = $derived.by(() => {
		const cp = sim.currentParams;
		const pp = sim.previousParams;
		if (!cp) return [];
		return [
			{ label: 'AL [μmol m⁻² s⁻¹]', newVal: cp.AL, oldVal: pp?.AL },
			{ label: 'SP [μmol m⁻² s⁻¹]', newVal: cp.SP, oldVal: pp?.SP },
			{ label: 'CtZ [s⁻¹]', newVal: cp.CtZ.toFixed(5), oldVal: pp?.CtZ?.toFixed(5) },
			{ label: 'CtV [s⁻¹]', newVal: cp.CtV.toFixed(6), oldVal: pp?.CtV?.toFixed(6) }
		];
	});

	let lineData = $derived.by(() => {
		if (sim.previousResult !== null) {
			return {
				labels: sim.currentResult?.time,
				datasets: [
					{
						label: 'new',
						data: sim.currentResult?.fluo ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: sim.previousResult?.fluo ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: sim.currentResult?.time,
			datasets: [
				{
					label: 'fluo',
					data: sim.currentResult?.fluo ?? [],
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
	let npqData = $derived.by(() => {
		if (sim.previousResult !== null) {
			return {
				labels: sim.currentResult?.npqTime,
				datasets: [
					{
						label: 'new',
						data: sim.currentResult?.npq ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: sim.previousResult?.npq ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: sim.currentResult?.npqTime,
			datasets: [
				{
					label: 'NPQ',
					data: sim.currentResult?.npq ?? [],
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
	let psiiData = $derived.by(() => {
		console.log('Updated');
		console.log($state.snapshot(sim.currentResult?.phiPsii));
		if (sim.previousResult !== null) {
			return {
				labels: sim.currentResult?.npqTime,
				datasets: [
					{
						label: 'new',
						data: sim.currentResult?.phiPsii ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: sim.previousResult?.phiPsii ?? [],
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: sim.currentResult?.npqTime,
			datasets: [
				{
					label: 'phi(PSII)',
					data: sim.currentResult?.phiPsii ?? [],
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
</script>

<svelte:head>
	<title>Dev</title>
</svelte:head>

<!-- Slider controls -------------------------------- -->
<div class="slider-section">
	<label class="slider-label">
		{@html m.slider_light()}: <strong>{lightIntensity}</strong>
		<input type="range" min="50" max="900" step="50" bind:value={lightIntensity} />
	</label>

	<div class="slider-row">
		<label class="slider-label">
			{@html m.fal_slider_time()}: <strong>{totalMinutes} min</strong>
			<input type="range" min="1" max="15" step="1" bind:value={totalMinutes} />
		</label>
		<label class="slider-label">
			{@html m.slider_pulses()}: <strong>{pulseInterval} s</strong>
			<input type="range" min="5" max="150" step="5" bind:value={pulseInterval} />
		</label>
	</div>

	{#if audienceStore.audience === '4bio'}
		<div class="slider-row">
			<div class="slider-col">
				<label class="slider-label">
					{@html m.slider_activation()}: <strong>{activationMultiplier}</strong>
					<input type="range" min="0" max="20" step="1" bind:value={activationIdx} />
				</label>
				<label class="slider-label">
					{@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
					<input type="range" min="0" max={totalMinutes * 60} step="5" bind:value={darkLength} />
				</label>
			</div>
			<div class="slider-col">
				<label class="slider-label">
					{@html m.slider_deactivation()}: <strong>{deactivationMultiplier}</strong>
					<input type="range" min="0" max="20" step="1" bind:value={deactivationIdx} />
				</label>
				<label class="slider-label">
					{@html m.fal_slider_saturate()}: <strong>{saturatingPulse}</strong>
					<input type="range" min="0" max="10000" step="500" bind:value={saturatingPulse} />
				</label>
			</div>
		</div>
	{/if}
</div>

<!-- Run controls -->
<div class="run-controls">
	<div class="run-btn-wrap">
		<Button loading={sim.loading} fullWidth onclick={runSimulation}>{sim.loading ? 'Running…' : 'Run simulation'}</Button>
	</div>
	<CompareCheckbox bind:checked={compareWithLast} />
</div>

{#if sim.errorMsg}
	<p class="error-msg">{sim.errorMsg}</p>
{/if}

<!-- Results ---------------------------------------- -->
{#if sim.currentResult}
	<div class="charts-section">
		<div class="charts-grid">
			<div class="chart-card">
				<p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
				<LineChart data={lineData} loading={false} {phases} yMax={1.2} />
			</div>

			<div class="chart-card">
				<p class="chart-label">{m.axis_npq()}</p>
				<LineChart data={npqData} loading={false} />
			</div>

			<div class="chart-card">
				<p class="chart-label">{m.axis_phipsii()}</p>
				<LineChart data={psiiData} loading={false} />
			</div>
		</div>

		{#if paramRows.length > 0}
			<div class="param-table-wrap">
				<ParameterTable
					rows={paramRows}
					showOld={showOld && sim.previousParams !== null}
					newLabel={m.new_label()}
					oldLabel={m.old_label()}
				/>
			</div>
		{/if}
	</div>
{/if}

<style>
	.slider-col {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
	}
</style>
