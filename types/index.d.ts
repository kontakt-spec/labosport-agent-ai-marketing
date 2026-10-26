export type StatusEtapu = 'czeka' | 'w_toku' | 'gotowe' | 'blad' | 'pominiete'

/** Zawartość `~/.labosport/stan.json` (postęp pracy na tym komputerze); pisze ją `lab.py stan`. */
export type StanPanelu = {
  event?: string
  kampania?: string
  plan?: string
  etap?: string
  etapy?: Record<string, StatusEtapu>
  postep?: { zrobione?: number; wszystkie?: number; opis?: string }
  czeka_na?: string | null
  agenci?: { nazwa: string; zadanie?: string; status?: string; od?: string }[]
  log?: { czas: string; tekst: string }[]
  aktualizacja?: string
}

/** Agent uruchomiony przez narzędzie Agent w tej sesji, widziany na żywo. */
export type AgentNaZywo = { nazwa: string; zadanie: string; status: 'pracuje' | 'gotowe' | 'blad'; od: number }

export type Dzialanie = { czas: number; tekst: string }

declare module 'claude-code' {
  interface PluginState {
    labosport: {
      stan: StanPanelu | null
      workspace: string | null
      link: string | null
      agenci: AgentNaZywo[]
      dzialania: Dzialanie[]
    }
  }
}
