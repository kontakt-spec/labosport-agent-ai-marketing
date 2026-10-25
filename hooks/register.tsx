import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { AgentNaZywo, Dzialanie, StanPanelu } from '../types'

// Panel "Agent AI Marketing": pokazuje etapy pracy, zespół agentów i ostatnie
// działania w Canvie i Postiz. Źródłem prawdy jest _system/stan.json w folderze
// roboczym (pisze go skrypt lab.py stan); wywołania narzędzi widzimy na żywo.

const PANE = 'labosport-agenci'
const TYTUL = 'Agent AI Marketing'

const stanA = atom({ plugin: 'labosport', key: 'stan' } as const, null)
const wsA = atom({ plugin: 'labosport', key: 'workspace' } as const, null)
const agenciA = atom({ plugin: 'labosport', key: 'agenci' } as const, [])
const dzialaniaA = atom({ plugin: 'labosport', key: 'dzialania' } as const, [])

const ETAPY: [string, string][] = [
  ['dane', 'Dane eventu'],
  ['plan', 'Plan komunikacji'],
  ['akceptacja_planu', 'Akceptacja planu'],
  ['grafiki', 'Grafiki w Canvie'],
  ['opisy', 'Opisy i komentarze'],
  ['kontrola', 'Kontrola jakości'],
  ['akceptacja_postow', 'Akceptacja postów'],
  ['postiz', 'Szkice w Postiz'],
]

const ZESPOL: [string, string, string][] = [
  ['analityk', 'Analityk', 'uczy się z historii eventu'],
  ['planista', 'Planista', 'układa plan komunikacji'],
  ['grafik', 'Grafik', 'robi grafiki w Canvie'],
  ['copywriter', 'Copywriter', 'pisze opisy i komentarze'],
  ['kontroler', 'Kontroler', 'sprawdza fakty i styl'],
  ['wydawca', 'Wydawca', 'wrzuca szkice do Postiz'],
]

const CANVA: Record<string, string> = {
  'search-designs': 'szukam projektów',
  'read-design': 'czytam projekt',
  'get-design': 'czytam projekt',
  'get-design-content': 'czytam treść projektu',
  'list-folder-items': 'przeglądam folder',
  'search-folders': 'szukam folderu',
  'create-folder': 'zakładam folder',
  'move-item-to-folder': 'porządkuję folder',
  'copy-design': 'kopiuję wzorzec',
  'edit-design': 'edytuję grafikę',
  'start-editing-transaction': 'otwieram grafikę do edycji',
  'perform-editing-operations': 'podmieniam tekst i zdjęcie',
  'commit-editing-transaction': 'zapisuję grafikę',
  'export-design': 'eksportuję grafikę',
  'upload-asset-from-url': 'wgrywam zdjęcie',
  'create-upload-url': 'wgrywam zdjęcie',
  'create-design': 'tworzę projekt',
  'resize-design': 'robię wersję story',
  'merge-designs': 'łączę strony',
  'get-assets': 'sprawdzam zdjęcia',
}

const POSTIZ: Record<string, string> = {
  integrationList: 'sprawdzam kanały',
  integrationSchema: 'sprawdzam ustawienia kanału',
  schedulePostTool: 'dodaję szkic posta',
  uploadFromUrlTool: 'wgrywam grafikę',
  postsListTool: 'czytam zaplanowane posty',
  mediaStatusTool: 'sprawdzam grafikę',
  postSettingsTool: 'sprawdzam ustawienia posta',
}

function godzina(ms: number): string {
  const d = new Date(ms)
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function pasek(zrobione: number, wszystkie: number, szerokosc: number): string {
  const w = Math.max(8, Math.min(30, szerokosc))
  const pelne = wszystkie > 0 ? Math.round((zrobione / wszystkie) * w) : 0
  return '█'.repeat(pelne) + '░'.repeat(w - pelne)
}

function katalog(sciezka: string): string {
  return sciezka.slice(0, sciezka.lastIndexOf('/'))
}

export const register: Register = on => {
  let ostatniStan = -1
  let sciezkaStanu: string | null = null

  on('session.start', async ($, e, next) => {
    const wynik = await next(e)

    await $.command.register({
      name: 'agenci',
      description: 'Otwiera panel Agent AI Marketing: etapy, agenci, postęp',
    })

    const home = await $.env.get('HOME')
    const odswiez = async () => {
      try {
        if (sciezkaStanu === null) {
          const konfig = `${home}/.labosport/config.json`
          if (!(await $.fs.exists(konfig))) return
          const ws = JSON.parse(await $.fs.read(konfig)).workspace as string | undefined
          if (!ws) return
          await update($, wsA, () => ws)
          sciezkaStanu = `${ws}/_system/stan.json`
        }
        if (!(await $.fs.exists(sciezkaStanu))) return
        const { mtimeMs } = await $.fs.stat(sciezkaStanu)
        if (mtimeMs === ostatniStan) return
        ostatniStan = mtimeMs
        const stan = JSON.parse(await $.fs.read(sciezkaStanu)) as StanPanelu
        await update($, stanA, () => stan)
      } catch {
        // Plik w trakcie zapisu albo jeszcze go nie ma: spróbujemy przy następnym tyknięciu.
      }
    }
    await odswiez()
    $.clock.every(2000, () => {
      void odswiez()
    })
    void $.ui.open({ id: PANE, title: TYTUL })

    return wynik
  })

  on('command.run', { command: 'agenci' }, async $ => {
    await $.ui.open({ id: PANE, title: TYTUL })
    return { text: 'Panel Agent AI Marketing otwarty.' }
  })

  on('tool.call', async ($, e, next) => {
    const narzedzie = String(e.tool)

    if (narzedzie === 'Agent' || narzedzie === 'Task') {
      const wejscie = e as unknown as { subagent_type?: string; description?: string }
      const typ = String(wejscie.subagent_type ?? '')
      if (!typ.startsWith('labosport:')) return next(e)
      const nazwa = typ.slice('labosport:'.length)
      const agent: AgentNaZywo = {
        nazwa,
        zadanie: String(wejscie.description ?? ''),
        status: 'pracuje',
        od: await $.clock.now(),
      }
      await update($, agenciA, lista => [...(lista ?? []).filter(a => a.nazwa !== nazwa), agent])
      const wynik = await next(e)
      const status: AgentNaZywo['status'] = wynik.deny !== undefined || wynik.isError === true ? 'blad' : 'gotowe'
      await update($, agenciA, lista => (lista ?? []).map(a => (a.nazwa === nazwa ? { ...a, status } : a)))
      return wynik
    }

    const krotka = narzedzie.includes('__') ? narzedzie.slice(narzedzie.lastIndexOf('__') + 2) : narzedzie
    const opis = CANVA[krotka] ? `Canva: ${CANVA[krotka]}` : POSTIZ[krotka] ? `Postiz: ${POSTIZ[krotka]}` : null
    if (opis) {
      const wpis: Dzialanie = { czas: await $.clock.now(), tekst: opis }
      await update($, dzialaniaA, lista => [...(lista ?? []), wpis].slice(-12))
    }
    return next(e)
  }).catch(($, e, next) => next(e)) // panel tylko obserwuje: jego błąd nigdy nie blokuje narzędzia

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const stan = await read($, stanA)
    const ws = await read($, wsA)
    const agenci = (await read($, agenciA)) ?? []
    const dzialania = (await read($, dzialaniaA)) ?? []
    const szer = e.props.bodyColumns ?? 40

    if (!ws) {
      return (
        <Box flexDirection="column" gap={1}>
          <Text bold>LABOSPORT · Agent AI Marketing</Text>
          <Text dimColor>
            System nie jest jeszcze skonfigurowany. Konfiguracja zakłada folder roboczy z folderami eventów i
            podłącza Canvę oraz Postiz.
          </Text>
          <Button key="start" variant="primary" onPress={() => $.prompt.submit({ text: '/labosport:start' })}>
            Rozpocznij konfigurację
          </Button>
        </Box>
      )
    }

    const etapy = stan?.etapy ?? {}
    const postep = stan?.postep
    const zStanu = new Map((stan?.agenci ?? []).map(a => [a.nazwa.toLowerCase(), a]))
    const naZywo = new Map(agenci.map(a => [a.nazwa.toLowerCase(), a]))

    return (
      <Box flexDirection="column" gap={1}>
        <Box flexDirection="column">
          <Text bold>{stan?.event ?? 'Brak aktywnej kampanii'}</Text>
          {stan?.kampania && <Text dimColor>{stan.kampania}</Text>}
        </Box>

        {stan?.czeka_na && (
          <Box borderStyle="round" borderColor="warning" paddingX={1}>
            <Text color="warning">Czeka na Was: {stan.czeka_na}</Text>
          </Box>
        )}

        <Box flexDirection="column">
          <Text dimColor>ETAPY</Text>
          {ETAPY.map(([klucz, etykieta]) => {
            const s = etapy[klucz] ?? 'czeka'
            const znak = s === 'gotowe' ? '✓' : s === 'w_toku' ? '●' : s === 'blad' ? '✕' : s === 'pominiete' ? '–' : '○'
            const kolor = s === 'gotowe' ? 'success' : s === 'w_toku' ? 'claude' : s === 'blad' ? 'error' : undefined
            return (
              <Text color={kolor} dimColor={s === 'czeka' || s === 'pominiete'} bold={stan?.etap === klucz}>
                {znak} {etykieta}
              </Text>
            )
          })}
        </Box>

        {postep && (postep.wszystkie ?? 0) > 0 && (
          <Box flexDirection="column">
            <Text>
              {pasek(postep.zrobione ?? 0, postep.wszystkie ?? 0, szer - 10)} {postep.zrobione ?? 0}/{postep.wszystkie}
            </Text>
            {postep.opis && <Text dimColor>{postep.opis}</Text>}
          </Box>
        )}

        <Box flexDirection="column">
          <Text dimColor>ZESPÓŁ AGENTÓW</Text>
          {ZESPOL.map(([klucz, nazwa, rola]) => {
            const zywy = naZywo.get(klucz)
            const zapis = zStanu.get(klucz)
            const status = zywy?.status ?? zapis?.status ?? 'czeka'
            const pracuje = status === 'pracuje' || status === 'w_toku'
            const zadanie = zywy?.zadanie || zapis?.zadanie || rola
            return (
              <Text color={pracuje ? 'claude' : status === 'gotowe' ? 'success' : undefined} dimColor={!pracuje && status !== 'gotowe'}>
                {pracuje ? '●' : status === 'gotowe' ? '✓' : '○'} {nazwa}: {pracuje ? zadanie : status === 'gotowe' ? 'gotowe' : rola}
              </Text>
            )
          })}
        </Box>

        {(dzialania.length > 0 || (stan?.log ?? []).length > 0) && (
          <Box flexDirection="column">
            <Text dimColor>OSTATNIE DZIAŁANIA</Text>
            {dzialania.slice(-5).map(d => (
              <Text dimColor>
                {godzina(d.czas)} {d.tekst}
              </Text>
            ))}
            {(stan?.log ?? []).slice(-4).map(l => (
              <Text dimColor>
                {l.czas.slice(11, 16)} {l.tekst}
              </Text>
            ))}
          </Box>
        )}

        <Box flexDirection="row" gap={1} flexWrap="wrap">
          {stan?.plan && (
            <Button key="plan" onPress={() => $.process.run(['open', `${katalog(stan.plan ?? '')}/plan.html`])}>
              Otwórz plan
            </Button>
          )}
          <Button key="folder" onPress={() => $.process.run(['open', ws])}>
            Folder eventów
          </Button>
          <Button key="dalej" variant="primary" onPress={() => $.prompt.submit({ text: '/labosport:marketing Co dalej?' })}>
            Co dalej?
          </Button>
        </Box>
      </Box>
    )
  })
}
