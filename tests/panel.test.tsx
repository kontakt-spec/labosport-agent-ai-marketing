import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'labosport',
  component: 'Pane',
  requestId: 'labosport-agenci',
  props: {
    title: 'Agent AI Marketing',
    isFocused: false,
    bodyColumns: 44,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

const STAN = {
  event: 'Castle Triathlon Malbork',
  kampania: 'listopad i grudzień 2026',
  etap: 'akceptacja_planu',
  etapy: { dane: 'gotowe', plan: 'gotowe', akceptacja_planu: 'w_toku' },
  czeka_na: 'Akceptacja planu',
  postep: { zrobione: 0, wszystkie: 18, opis: 'Plan do akceptacji' },
  agenci: [{ nazwa: 'planista', status: 'gotowe' }],
  log: [{ czas: '2026-10-25T15:40:00', tekst: 'Plan gotowy' }],
}

test('panel pokazuje event, bramkę akceptacji i agenta, który pracuje', async ($, on) => {
  on('command.register', () => ({ value: { command: 'agenci' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('env.get', () => ({ value: '/Users/test' }))
  on('fs.exists', () => ({ value: true }))
  on('fs.stat', () => ({ value: { kind: 'file', size: 10, mtimeMs: 1, isLink: false } }))
  on('fs.read', (_, e) => ({
    value: e.path.endsWith('config.json') ? JSON.stringify({ workspace: '/ws' }) : JSON.stringify(STAN),
  }))
  on('tool.call', () => ({ result: {} }))
  on('clock.now', () => ({ value: Date.UTC(2026, 9, 25, 14, 40) }))
  on('clock.every', () => ({ value: undefined }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: 'mcp__canva__copy-design', design_id: 'DAAAAAAAAAA' } as never)

  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect(await ui.find({ type: 'Text', text: /Castle Triathlon Malbork/ })).toBeDefined()
    expect((await ui.find({ type: 'Text', text: /Czeka na Was/ }))?.text).toContain('Akceptacja planu')
    expect((await ui.find({ type: 'Text', text: /Planista/ }))?.text).toContain('gotowe')
    expect((await ui.find({ type: 'Text', text: /Canva: kopiuję wzorzec/ }))?.text).toContain('Canva')
    await ui.unmount()
  }
})

test('bez konfiguracji panel prowadzi do /labosport:start', async ($, on) => {
  on('command.register', () => ({ value: { command: 'agenci' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('env.get', () => ({ value: '/Users/test' }))
  on('fs.exists', () => ({ value: false }))
  on('clock.every', () => ({ value: undefined }))

  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect(await ui.find({ key: 'start' })).toBeDefined()
  await ui.unmount()
})
