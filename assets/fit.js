/* The sofa fit calculator on getscooch.com/sofa-fit-calculator/.
   Runs entirely in the browser: nothing typed here is sent anywhere. Analytics get the
   outcome only (fits, tilt, no), never a measurement. The maths sits on top, free of the
   page, so _gen/test_fit.js can check it with `jsc`. Everything is in centimetres inside. */
(function (root) {
  'use strict';

  var TIGHT_CM = 2.5;   // under this much to spare, a moving blanket can be the difference

  // The longest box of width w that can be carried LEVEL round a right-angle corner, from a
  // hallway a wide into one b wide. Tilted at angle t, its outer long edge runs from the
  // outer wall of one hallway to the outer wall of the other while its inner edge touches
  // the inner corner, which gives L(t) = a/sin t + b/cos t - w/(sin t cos t). The longest
  // box that gets round is the smallest L(t). Checks: w = 0 is the ladder answer
  // (a^(2/3) + b^(2/3))^(3/2); a = b gives 2(a*sqrt(2) - w).
  function maxLengthRoundCorner(a, b, w) {
    if (!(a > 0 && b > 0) || !(w >= 0) || w >= a || w >= b) return 0;
    var best = Infinity, steps = 9000;
    for (var i = 1; i < steps; i++) {
      var t = (i / steps) * (Math.PI / 2);
      var s = Math.sin(t), c = Math.cos(t);
      var len = a / s + b / c - w / (s * c);
      if (len < best) best = len;
    }
    return Math.max(0, best);
  }

  // Through a doorway, straight on. The sofa goes through length first, so the opening sees
  // its depth and its height. Upright: depth across, height up. On its back: height across,
  // depth up. Failing both, the shop-floor test: a diagonal depth narrower than the opening
  // means it can be tipped back and swung through.
  function doorCheck(sofa, door) {
    var options = [];
    if (sofa.depth <= door.width && sofa.height <= door.height) {
      options.push({ how: 'upright', spare: door.width - sofa.depth });
    }
    if (sofa.height <= door.width && sofa.depth <= door.height) {
      options.push({ how: 'back', spare: door.width - sofa.height });
    }
    if (options.length) {
      // Upright is how people carry a sofa; on its back only when upright is tight.
      var upright = options[0].how === 'upright' && options[0].spare >= TIGHT_CM;
      if (!upright) options.sort(function (x, y) { return y.spare - x.spare; });
      return { fits: true, how: options[0].how, spare: options[0].spare };
    }
    if (sofa.diag > 0 && sofa.diag <= door.width) {
      return { fits: true, how: 'tilt', spare: door.width - sofa.diag };
    }
    return { fits: false, over: Math.min(sofa.depth, sofa.height) - door.width };
  }

  // A turn before the door. Carried level, the box's narrow side is its depth (upright) or
  // its height (on its back), whichever is smaller. Stood on its end, the length goes up,
  // so it needs the ceiling, and what has to turn is only depth by height.
  function cornerCheck(sofa, hallA, hallB, ceiling) {
    var narrow = Math.min(sofa.depth, sofa.height);
    var wide = Math.max(sofa.depth, sofa.height);
    if (narrow >= hallA) return { fits: false, how: 'none', blocked: 'before', limit: 0 };
    if (narrow >= hallB) return { fits: false, how: 'none', blocked: 'after', limit: 0 };
    var limit = maxLengthRoundCorner(hallA, hallB, narrow);
    if (sofa.width <= limit) return { fits: true, how: 'level', limit: limit };
    if (ceiling > 0 && sofa.width <= ceiling && limit >= wide) {
      return { fits: true, how: 'end', limit: limit };
    }
    return { fits: false, how: 'long', limit: limit };
  }

  root.ScoochFit = { maxLengthRoundCorner: maxLengthRoundCorner, doorCheck: doorCheck,
                     cornerCheck: cornerCheck, TIGHT_CM: TIGHT_CM };

  if (typeof document === 'undefined') return;

  // ---------------------------------------------------------------- the page
  var form = document.getElementById('fit-form');
  if (!form) return;
  var out = document.getElementById('fit-result');
  var unit = 'cm';

  function num(id) {
    var v = parseFloat(String(document.getElementById(id).value).replace(',', '.'));
    if (!(v > 0)) return 0;
    return unit === 'in' ? v * 2.54 : v;
  }
  function fmt(cm) {
    return unit === 'in' ? (cm / 2.54).toFixed(1) + ' in' : Math.round(cm) + ' cm';
  }
  function line(kind, html) {
    return '<p class="fit-line fit-' + kind + '">' + html + '</p>';
  }

  function setUnit(next) {
    if (next === unit) return;
    form.querySelectorAll('input[type="number"]').forEach(function (el) {
      var v = parseFloat(el.value);
      if (v > 0) el.value = next === 'in' ? (v / 2.54).toFixed(1) : String(Math.round(v * 2.54));
    });
    unit = next;
    form.querySelectorAll('.unit-label').forEach(function (el) { el.textContent = next; });
    form.querySelectorAll('input[name="unit"]').forEach(function (el) { el.checked = el.value === next; });
  }

  form.querySelectorAll('input[name="unit"]').forEach(function (el) {
    el.addEventListener('change', function () { if (el.checked) setUnit(el.value); });
  });
  try {
    if (/^en-(US|LR|MM)$/i.test(navigator.language || '')) setUnit('in');
  } catch (e) {}

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var legs = num('legs');
    var sofa = { width: num('sofa-w'), depth: num('sofa-d'), height: num('sofa-h'), diag: num('sofa-dd') };
    if (legs > 0 && legs < sofa.height) sofa.height -= legs;
    var door = { width: num('door-w'), height: num('door-h') || 200 };
    var hallA = num('hall-a'), hallB = num('hall-b') || door.width, ceiling = num('ceiling');

    if (!sofa.width || !sofa.depth || !sofa.height || !door.width) {
      out.innerHTML = line('warn', 'Fill in the sofa\'s width, depth and height, and the width of the doorway.');
      return;
    }

    var html = '', outcome = {};
    var d = doorCheck(sofa, door);
    if (d.fits && d.how === 'tilt') {
      outcome.door = 'tilt';
      html += line('ok', '<strong>Through the door: yes, tipped back.</strong> It is too deep to go straight through, but its diagonal depth is ' + fmt(d.spare) + ' narrower than the opening. Tip it back so that diagonal lines up with the gap, and swing it through.');
    } else if (d.fits) {
      outcome.door = d.spare < TIGHT_CM ? 'tight' : 'yes';
      var how = d.how === 'upright' ? 'carried upright' : 'on its back (the back lying flat)';
      if (d.spare < TIGHT_CM) {
        html += line('warn', '<strong>Through the door: only just.</strong> ' + capital(how) + ', it has ' + fmt(d.spare) + ' to spare. A moving blanket or a door handle can eat that, so take the door off its hinges if you can.');
      } else {
        html += line('ok', '<strong>Through the door: yes.</strong> ' + capital(how) + ', with ' + fmt(d.spare) + ' to spare.');
      }
    } else {
      outcome.door = 'no';
      var tip = sofa.diag ? '' : ' Measure its diagonal depth too: if that is narrower than the doorway, it can be tipped through.';
      html += line('no', '<strong>Through the door: no, by ' + fmt(d.over) + '.</strong> Before you give up: take the legs off, take the door off its hinges, and ask the shop whether the back or the arms come off.' + tip);
    }

    if (hallA > 0) {
      var c = cornerCheck(sofa, hallA, hallB, ceiling);
      if (c.how === 'none' && c.blocked === 'after' && !num('hall-b') && d.how === 'tilt') {
        // The door takes it only tipped back, and the turn maths is for carrying it level.
        outcome.corner = 'unknown';
        html += line('warn', '<strong>The turn: can\'t tell.</strong> This door only takes it tipped back, and the turn maths here is for carrying it level. Leave room in the hallway to tip it and swing it, and try the route with a tape first.');
      } else if (c.how === 'none') {
        outcome.corner = 'no';
        html += line('no', c.blocked === 'before'
          ? '<strong>The turn: no.</strong> Carried level, the sofa is wider than the hallway, before it even gets to the turn.'
          : '<strong>The turn: no.</strong> Carried level, the sofa is wider than the opening after the turn.');
      } else if (c.how === 'level') {
        outcome.corner = 'yes';
        html += line('ok', '<strong>The turn: yes.</strong> Carried level, the longest sofa that makes this turn is about ' + fmt(c.limit) + '. Yours is ' + fmt(sofa.width) + '.');
      } else if (c.how === 'end') {
        outcome.corner = 'end';
        html += line('ok', '<strong>The turn: yes, stood on its end.</strong> Carried level it is too long (the limit is about ' + fmt(c.limit) + '), but on its end it is ' + fmt(sofa.width) + ' tall under a ' + fmt(ceiling) + ' ceiling, and the turn gets easy.');
      } else {
        outcome.corner = 'no';
        var ceil = ceiling > 0 ? ' It is also taller than the ceiling on its end.' : ' Movers often get round a tight turn by standing the sofa on its end: add the ceiling height to check that.';
        html += line('no', '<strong>The turn: no, carried level.</strong> The longest sofa that makes this turn is about ' + fmt(c.limit) + ', and yours is ' + fmt(sofa.width) + '.' + ceil);
      }
    }

    html += '<p class="fit-note">Flat-floor maths with the numbers you typed. Within a few centimetres, measure again: skirting boards, door stops and handles all take their share.</p>';
    out.innerHTML = html;
    try {
      if (window.posthog && typeof posthog.capture === 'function') {
        posthog.capture('fit_check', { door: outcome.door, corner: outcome.corner || 'skipped' });
      }
    } catch (e) {}
  });

  function capital(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
})(this);
