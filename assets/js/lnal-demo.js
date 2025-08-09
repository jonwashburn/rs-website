// LNAL instruction runner (toy model)
const PHI = (1 + Math.sqrt(5)) / 2;

const INSTR = [
  'LISTEN', 'LOCK', 'FOLD', 'GIVE', 'REGIVE', 'UNFOLD', 'BALANCE', 'ECHO'
];

function format(x, n = 3) {
  return Number(x).toFixed(n);
}

function J(x) {
  return 0.5 * (x + 1 / x);
}

function select(id) {
  return document.getElementById(id);
}

function setActiveCycle(idx) {
  const list = document.getElementById('cycle-list');
  if (!list) return;
  Array.from(list.children).forEach((li, i) => {
    if (i === idx) li.classList.add('active');
    else li.classList.remove('active');
  });
}

function initDemo() {
  const root = document.getElementById('lnal-demo');
  if (!root) return;

  // Register state (toy)
  const state = {
    tick: 0,
    nu: 1.0, // νφ frequency scale
    ell: 0,
    sigma: +1,
    tau: 0,
    kp: 0,
    phi_e: 0,
    x: 1.0, // cost argument
  };

  function updateUI() {
    select('demo-tick').textContent = String(state.tick);
    select('demo-instr').textContent = INSTR[state.tick % 8] || '—';
    select('reg-nu').textContent = format(state.nu);
    select('reg-ell').textContent = String(state.ell);
    select('reg-sigma').textContent = state.sigma > 0 ? '+1' : '-1';
    select('reg-tau').textContent = String(state.tau);
    select('reg-kp').textContent = String(state.kp);
    select('reg-phi').textContent = String(state.phi_e);
    select('cost-x').textContent = format(state.x);
    select('cost-j').textContent = format(J(state.x));
    setActiveCycle(state.tick % 8);
  }

  function stepForward() {
    const i = state.tick % 8;
    switch (INSTR[i]) {
      case 'LISTEN':
        // quiet read: reduce x towards 1
        state.x = (state.x + 1) / 2;
        state.tau += 1;
        break;
      case 'LOCK':
        // create a token: bump ell (structure)
        state.ell += 1;
        state.x = Math.max(state.x, 1.0) + 0.05;
        break;
      case 'FOLD':
        // focus up by φ
        state.nu *= PHI;
        state.x *= PHI;
        break;
      case 'GIVE':
        // project attention: flip sigma if large x
        if (state.x > 1.2) state.sigma *= -1;
        state.kp += 1;
        break;
      case 'REGIVE':
        // receive reflection: move x back toward 1
        state.x = 1 + (state.x - 1) / PHI;
        break;
      case 'UNFOLD':
        // relax by 1/φ
        state.nu /= PHI;
        state.x /= PHI;
        break;
      case 'BALANCE':
        // close token: reduce ell and pull x to 1
        state.ell = Math.max(0, state.ell - 1);
        state.x = (state.x + 1) / 2;
        break;
      case 'ECHO':
        // consolidate: nudge phi_e and reset kp
        state.phi_e = (state.phi_e + 1) % 8;
        state.kp = 0;
        break;
    }
    state.tick = (state.tick + 1) % 8;
    updateUI();
  }

  function stepBack() {
    // simple reverse: just move pointer back for UI purposes
    state.tick = (state.tick + 7) % 8;
    updateUI();
  }

  function reset() {
    state.tick = 0;
    state.nu = 1.0;
    state.ell = 0;
    state.sigma = +1;
    state.tau = 0;
    state.kp = 0;
    state.phi_e = 0;
    state.x = 1.0;
    updateUI();
  }

  select('demo-step').addEventListener('click', stepForward);
  select('demo-prev').addEventListener('click', stepBack);
  select('demo-reset').addEventListener('click', reset);

  reset();
}

document.addEventListener('DOMContentLoaded', initDemo);


