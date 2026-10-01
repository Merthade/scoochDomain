// Checks the calculator's maths. Run: jsc _gen/test_fit.js  (from the site root)
load('assets/fit.js');
var F = ScoochFit, fails = 0;
function near(name, got, want, tol) {
  var ok = Math.abs(got - want) <= tol;
  if (!ok) fails++;
  print((ok ? 'PASS ' : 'FAIL ') + name + ': got ' + got.toFixed(2) + ', want ' + want.toFixed(2));
}
function is(name, got, want) {
  var ok = got === want;
  if (!ok) fails++;
  print((ok ? 'PASS ' : 'FAIL ') + name + ': got ' + got + ', want ' + want);
}
// Ladder (w = 0): (a^(2/3) + b^(2/3))^(3/2)
near('ladder 100/100', F.maxLengthRoundCorner(100, 100, 0), Math.pow(2 * Math.pow(100, 2 / 3), 1.5), 0.05);
near('ladder 90/120', F.maxLengthRoundCorner(90, 120, 0), Math.pow(Math.pow(90, 2 / 3) + Math.pow(120, 2 / 3), 1.5), 0.05);
// Equal hallways with width: 2(a*sqrt(2) - w)
near('box 100/100 w50', F.maxLengthRoundCorner(100, 100, 50), 2 * (100 * Math.SQRT2 - 50), 0.05);
near('box 90/90 w85', F.maxLengthRoundCorner(90, 90, 85), 2 * (90 * Math.SQRT2 - 85), 0.05);
// Symmetric in a and b
near('symmetry', F.maxLengthRoundCorner(80, 110, 40), F.maxLengthRoundCorner(110, 80, 40), 0.01);
// Wider than a hallway: nothing gets round
is('too wide', F.maxLengthRoundCorner(80, 100, 85), 0);
// Doors: a 210 x 90 x 85 sofa through an 80 cm door: neither way, diagonal 78 tips through
var sofa = { width: 210, depth: 90, height: 85, diag: 78 };
var d = F.doorCheck(sofa, { width: 80, height: 200 });
is('tilt fits', d.fits && d.how, 'tilt');
near('tilt spare', d.spare, 2, 1e-9);
d = F.doorCheck({ width: 210, depth: 90, height: 85, diag: 0 }, { width: 80, height: 200 });
is('no diag: no', d.fits, false);
near('over by', d.over, 5, 1e-9);
d = F.doorCheck(sofa, { width: 88, height: 200 });
is('on its back', d.how, 'back');
near('back spare', d.spare, 3, 1e-9);
d = F.doorCheck(sofa, { width: 95, height: 200 });
is('upright preferred when it has room', d.how, 'upright');
d = F.doorCheck(sofa, { width: 91, height: 200 });
is('upright tight (1 cm): roomier back wins', d.how, 'back');
// Corner: 210 cm sofa, 85 narrow, 100 cm hall into an 80 cm door: 2-sided limit
var c = F.cornerCheck(sofa, 100, 100, 0);
near('corner limit', c.limit, 2 * (100 * Math.SQRT2 - 85), 0.05);
is('corner too long level', c.how, 'long');
c = F.cornerCheck(sofa, 100, 100, 240);
is('on its end under 240', c.how, 'end');
c = F.cornerCheck({ width: 150, depth: 80, height: 75 }, 110, 100, 0);
is('150 loveseat, 110/100 hall: limit ~147, too long', c.how, 'long');
c = F.cornerCheck({ width: 140, depth: 80, height: 75 }, 110, 100, 0);
is('140 loveseat turns level', c.how, 'level');
c = F.cornerCheck(sofa, 100, 80, 240);
is('door narrower than the narrow side: blocked after', c.blocked, 'after');
c = F.cornerCheck(sofa, 80, 100, 0);
is('hallway narrower than the narrow side: blocked before', c.blocked, 'before');
print(fails ? fails + ' FAILED' : 'all passed');
if (fails) throw new Error('fit tests failed');
