<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import {
		Chart,
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		Title,
		Tooltip,
		Legend,
		Filler
	} from 'chart.js';

	Chart.register(
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		Title,
		Tooltip,
		Legend,
		Filler
	);

	export interface PhaseRegion {
		start: number;
		end: number;
		color: string;
		label?: string;
	}

	interface Props {
		/** X-axis data in seconds (for new run) */
		xNew: number[];
		/** Y-axis data (for new run) */
		yNew: number[];
		/** X-axis data for old run (optional) */
		xOld?: number[];
		/** Y-axis data for old run (optional) */
		yOld?: number[];
		/** Background phase regions */
		phases?: PhaseRegion[];
		/** Y-axis label */
		yLabel?: string;
		/** Whether to connect data points with a line (true) or show as scatter (false) */
		showLine?: boolean;
		/** Total time range for x axis (seconds) */
		totalTime?: number;
	}

	let {
		xNew,
		yNew,
		xOld = [],
		yOld = [],
		phases = [],
		yLabel = '',
		showLine = true,
		totalTime
	}: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;

	const NEW_COLOR = '#FF4B4B';
	const OLD_COLOR = 'rgba(255, 75, 75, 0.5)';

	// Custom plugin for background phase shading + labels
	const phaseShadingPlugin = {
		id: 'phaseShading',
		beforeDraw(ch: Chart) {
			if (!phases.length) return;
			const { ctx, chartArea, scales } = ch;
			if (!chartArea || !scales.x) return;
			const { left, right, top, bottom } = chartArea;
			const height = bottom - top;

			ctx.save();
			ctx.beginPath();
			ctx.rect(left, top, right - left, height);
			ctx.clip();

			for (const phase of phases) {
				const xStart = Math.max(scales.x.getPixelForValue(phase.start), left);
				const xEnd = Math.min(scales.x.getPixelForValue(phase.end), right);
				if (xEnd <= xStart) continue;

				ctx.fillStyle = phase.color;
				ctx.fillRect(xStart, top, xEnd - xStart, height);

				if (phase.label && phase.end > phase.start) {
					const midX = (xStart + xEnd) / 2;
					ctx.fillStyle = 'rgba(0,0,0,0.5)';
					ctx.font = '11px system-ui, sans-serif';
					ctx.textAlign = 'center';
					ctx.fillText(phase.label, midX, top + 14);
				}
			}

			ctx.restore();
		}
	};

	function buildDatasets() {
		const datasets = [];

		if (xNew.length && yNew.length) {
			const data = xNew.map((x, i) => ({ x, y: yNew[i] }));
			datasets.push({
				label: 'New',
				data,
				parsing: false as const,
				borderColor: NEW_COLOR,
				backgroundColor: NEW_COLOR,
				borderWidth: 2,
				pointRadius: showLine ? 0 : 4,
				pointHoverRadius: 4,
				showLine,
				tension: 0
			});
		}

		if (xOld.length && yOld.length) {
			const data = xOld.map((x, i) => ({ x, y: yOld[i] }));
			datasets.push({
				label: 'Old',
				data,
				parsing: false as const,
				borderColor: OLD_COLOR,
				backgroundColor: OLD_COLOR,
				borderWidth: 2,
				pointRadius: showLine ? 0 : 4,
				pointHoverRadius: 4,
				showLine,
				tension: 0,
				borderDash: [6, 3]
			});
		}

		return datasets;
	}

	function getXMax() {
		if (totalTime !== undefined) return totalTime;
		const allX = [...xNew, ...xOld];
		return allX.length ? Math.max(...allX) : 300;
	}

	function createChart() {
		if (!canvas) return;
		if (chart) chart.destroy();

		const xMax = getXMax();

		chart = new Chart(canvas, {
			type: 'line',
			plugins: [phaseShadingPlugin],
			data: { datasets: buildDatasets() },
			options: {
				animation: false,
				responsive: true,
				maintainAspectRatio: true,
				interaction: { mode: 'nearest', axis: 'x', intersect: false },
				scales: {
					x: {
						type: 'linear',
						position: 'bottom',
						min: 0,
						max: xMax,
						title: { display: true, text: 'Time [s]' },
						border: { display: true },
						grid: { display: false }
					},
					x2: {
						type: 'linear',
						position: 'top',
						min: 0,
						max: xMax / 60,
						title: { display: true, text: 'Time [min]' },
						border: { display: false },
						grid: { display: false },
						ticks: {
							callback: (v) => (typeof v === 'number' ? v.toFixed(1) : v)
						}
					},
					y: {
						type: 'linear',
						title: { display: !!yLabel, text: yLabel },
						border: { display: true },
						grid: { color: 'rgba(0,0,0,0.05)' }
					}
				},
				plugins: {
					legend: { display: false },
					tooltip: {
						callbacks: {
							label: (ctx) => `${ctx.dataset.label}: ${(ctx.parsed.y as number).toFixed(3)}`
						}
					}
				}
			}
		});
	}

	function updateChart() {
		if (!chart) return;
		const xMax = getXMax();
		chart.data.datasets = buildDatasets();
		if (chart.options.scales?.x) {
			chart.options.scales.x.max = xMax;
		}
		if (chart.options.scales?.x2) {
			chart.options.scales.x2.max = xMax / 60;
		}
		chart.update();
	}

	onMount(() => {
		createChart();
	});

	onDestroy(() => {
		chart?.destroy();
	});

	$effect(() => {
		// Re-read reactive props to establish dependency
		void xNew;
		void yNew;
		void xOld;
		void yOld;
		void phases;
		void totalTime;
		if (chart) {
			updateChart();
		} else {
			createChart();
		}
	});
</script>

<div class="chart-wrapper">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.chart-wrapper {
		position: relative;
		width: 100%;
	}
</style>
