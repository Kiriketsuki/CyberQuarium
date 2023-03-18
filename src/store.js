// store.js
import { writable } from 'svelte/store';

export const user = writable(null);
export const currentPage = writable('landing'); // Add this line
