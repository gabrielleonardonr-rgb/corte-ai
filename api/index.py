async function claude(prompt, sys) {
  const r = await fetch(`${API}/claude`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      system: sys,
      messages: [{ role: 'user', content: prompt }]
    })
  });
  const d = await r.json();
  return JSON.parse(
    d.content.map(i => i.text || '').join('').replace(/```json|```/g, '').trim()
  );
}
