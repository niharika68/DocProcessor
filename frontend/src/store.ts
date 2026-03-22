import { atom } from "jotai";
import type { ProcessResponse, Annotation, DocType } from "./types";

export const activeTabAtom = atom<DocType>("invoice");

// Per-tab result state
export const invoiceResultAtom = atom<ProcessResponse | null>(null);
export const contractResultAtom = atom<ProcessResponse | null>(null);
export const referralResultAtom = atom<ProcessResponse | null>(null);

export const loadingAtom = atom<boolean>(false);
export const errorAtom = atom<string | null>(null);

export const selectedAnnotationAtom = atom<Annotation | null>(null);
