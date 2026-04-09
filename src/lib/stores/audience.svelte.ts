import { browser } from '$app/environment';

export type Audience = '4bio' | '4math';

const STORAGE_KEY = 'comphot-audience';

function readStored(): Audience {
	if (browser) {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored === '4bio' || stored === '4math') return stored;
	}
	return '4bio';
}

class AudienceStore {
	audience = $state<Audience>(readStored());

	setAudience(v: Audience) {
		this.audience = v;
		if (browser) {
			localStorage.setItem(STORAGE_KEY, v);
		}
	}
}

export const audienceStore = new AudienceStore();
