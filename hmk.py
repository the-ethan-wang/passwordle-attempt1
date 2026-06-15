import math
import z3
import sys


sequence = [
  0.03496367955700219,
  0.6611341003944247,
  0.7700628052494365,
  0.8088536322578446,
  0.04670808464549192,
  0.2967115504914406,
  0.0736202321761763,
  0.636302812358886,
  0.804365927922012,
  0.7859885898991928,
  0.46818916934249855,
  0.5067502311263505,
  0.5823980066386926,
  0.8982276327207052,
  0.05018293923159689,
  0.6567148856052191,
  0.653175048970716,
  0.755565805342348,
  0.1609927508893748,
  0.5548140353832507,
  0.46863524825924086,
  0.4053742389200965,
  0.3670368393149669,
  0.5393162358759921,
  0.37456121800267184,
  0.33647273578428816,
  0.17119682792990443,
  0.7209587775806006,
  0.5205902345298198,
  0.18945882201261155,
  0.007936481079643731,
  0.107338694901423,
  0.04897595912799391,
  0.6743333045406635,
  0.007902083077831246,
  0.5722661223464931,
  0.05657317592770239,
  0.4406721074267361,
  0.5693962276613458,
  0.6963461218835106,
  0.8821614670632172,
  0.28165090870794307,
  0.6605990430012791,
  0.18817810117173261,
  0.6204098549072454,
  0.6180345182946783,
  0.9382259041020952,
  0.033484208077536604,
  0.4209229941781525,
  0.30344577035013365
]
def get_states():
  solver = z3.Solver()

  se_state0, se_state1 = z3.BitVecs("se_state0 se_state1", 64)

  for i in range(len(sequence)):
    se_s1 = se_state0
    se_s0 = se_state1
    se_s1 ^= se_s1 << 23
    se_s1 ^= z3.LShR(se_s1, 17)  # Logical shift instead of Arthmetric shift
    se_s1 ^= se_s0
    se_s1 ^= z3.LShR(se_s0, 26)
    se_state0 = se_state1
    se_state1 = se_s1
    calc = se_state1 + se_state0

    # Get the lower 52 bits (mantissa)
    mantissa = sequence[i] * (0x1 << 53)

    # Compare Mantissas
    solver.add(int(mantissa) == (calc & 0x1FFFFFFFFFFFFF))

  if solver.check() == z3.sat:
    model = solver.model()

    states = {}
    for state in model.decls():
      states[state.__str__()] = model[state]

    print(states)
    return states
  print('oops')

MASK = 0xFFFFFFFFFFFFFFFF

def next(state0, state1):
  s1 = state0 & MASK
  s0 = state1 & MASK
  s1 ^= (s1 << 23) & MASK
  s1 ^= (s1 >> 17) & MASK
  s1 ^= s0 & MASK
  s1 ^= (s0 >> 26) & MASK 
  state0 = state1 & MASK
  state1 = s1 & MASK
  gen = (state0 + state1) & MASK
  return state0, state1, gen
states = get_states()

state0 = states["se_state0"].as_long()
state1 = states["se_state1"].as_long()

for i in range(len(sequence)):
  state0, state1, out = next(state0, state1)

ans=[]

for i in range(50):
  state0, state1, out = next(state0, state1)

  double = float(out & 0x1FFFFFFFFFFFFF) / (0x1 << 53) 

  ans.append(double)
print(*ans,sep="\n")
def randompassword():
  letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  digits = "0123456789"
  punctuation = r"""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
  s = letters*7+digits*4+punctuation*3
  length = 14
  res = [s[math.floor(ans[i]*len(s))] for i in range(length)]
  print("".join(res))

randompassword()