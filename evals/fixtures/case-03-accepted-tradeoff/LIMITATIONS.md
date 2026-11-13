# Known limitations (maintainer-stated, binding on reviewers)

- The replay engine (sync window loop) and the live engine (async polled
  sample) share decision code but interpret it differently. A shared-trace
  parity contract was proposed in issue #1042 and declined: recording
  sample-level traces for 50 services over a year costs hundreds of GB of
  storage, and the team accepts documented divergence instead. Do not
  re-propose it as a fresh defect.
