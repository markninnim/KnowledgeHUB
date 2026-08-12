// Regenerates public/static/git-log-export.txt AND public/static/git-log-stats.json
// from the current git history. Run automatically on every deploy (see
// package.json "postinstall") so both fallback files stay current, even
// though Railway's runtime container doesn't ship the .git folder (only the
// build step does).
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Date KnowledgeHUB was granted MVP status (v2.0 milestone) — see
// public/version-history.html.
const MVP_DATE = '2026-07-17';

try {
  const out = execFileSync('git', ['log', '--all', '--date=short', '--pretty=format:%ad | %h | %s'], {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf8',
    maxBuffer: 20 * 1024 * 1024
  });
  const lines = out.split('\n').filter(Boolean);
  const dates = lines.map(l => l.slice(0, 10)).sort();
  const header = [
    'KnowledgeHUB — Full Git Commit Log Export',
    `Generated: ${new Date().toISOString().slice(0, 10)}`,
    `Total commits: ${lines.length}`,
    `Range: ${dates[0]} to ${dates[dates.length - 1]}`,
    '='.repeat(60),
    ''
  ].join('\n');
  const outPath = path.join(__dirname, '..', 'public/static/git-log-export.txt');
  fs.writeFileSync(outPath, header + out);
  console.log(`git-log-export.txt regenerated: ${lines.length} commits, ${dates[0]} to ${dates[dates.length - 1]}`);
} catch (err) {
  console.warn('generate-git-log: export skipped (git unavailable in this environment):', err.message);
}

try {
  const raw = execFileSync('git', ['log', '--all', '--pretty=format:%ai'], {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf8',
    maxBuffer: 20 * 1024 * 1024
  });
  const rows = raw.split('\n').filter(Boolean).map(l => {
    // "2026-08-12 08:56:24 +0100"
    const date = l.slice(0, 10);
    const hour = parseInt(l.slice(11, 13), 10);
    const d = new Date(l.slice(0, 19).replace(' ', 'T'));
    const weekday = d.getDay(); // 0=Sun..6=Sat
    return { date, hour, weekday };
  });

  const byHour = new Array(24).fill(0);
  const byWeekday = new Array(7).fill(0); // 0=Sun..6=Sat
  const bucket = (rows, cutoffBefore) => {
    const set = cutoffBefore ? rows.filter(r => r.date < cutoffBefore) : rows;
    let within = 0, weekend = 0, weekdayOutside = 0;
    set.forEach(r => {
      const isWeekend = r.weekday === 0 || r.weekday === 6;
      const inHours = r.hour >= 9 && r.hour < 17;
      if (isWeekend) weekend++;
      else if (!inHours) weekdayOutside++;
      else within++;
    });
    const total = set.length;
    const outside = weekend + weekdayOutside;
    return { total, within, outside, weekend, weekdayOutside };
  };

  rows.forEach(r => {
    byHour[r.hour]++;
    byWeekday[r.weekday]++;
  });

  const stats = {
    generatedAt: new Date().toISOString().slice(0, 10),
    mvpDate: MVP_DATE,
    overall: bucket(rows, null),
    preMvp: bucket(rows, MVP_DATE),
    byHour,
    byWeekday
  };

  const statsPath = path.join(__dirname, '..', 'public/static/git-log-stats.json');
  fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2));
  console.log(`git-log-stats.json regenerated: ${stats.overall.total} commits (${stats.overall.outside} outside Mon-Fri 9-5), ${stats.preMvp.total} pre-MVP`);
} catch (err) {
  console.warn('generate-git-log: stats skipped (git unavailable in this environment):', err.message);
}
