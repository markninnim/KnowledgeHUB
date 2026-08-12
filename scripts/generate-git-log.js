// Regenerates public/static/git-log-export.txt from the current git history.
// Run automatically on every deploy (see package.json "postinstall") so the
// fallback file used by /api/git-log never goes stale, even though Railway's
// runtime container doesn't ship the .git folder (only the build step does).
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

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
  console.warn('generate-git-log: skipped (git unavailable in this environment):', err.message);
}
