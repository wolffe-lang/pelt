Oracle recording image (pelt#69)

BLOCKED, not an available image or a completed CI gate.
On 2026-10-26 the Arch archive contains bash 5.3.20-1, not the required
bash 5.3.20-2. The latter URL returns HTTP 404. Do not substitute -1.
packages.sha256 pins the available dash and fish archives; UNAVAILABLE
is deliberately fatal before downloads, build or package installation.
The base is a registry digest, not a rolling tag. All packages are exact
archive URLs. No pacman -Syu, host installation or registry publication.

After the exact bash package is available, record its digest, resolve and
pin every missing dependency the same way (including Python for the corpus
runner if not already in the base), and prove all three versions inside
the image. Only then add the workflow_dispatch-only recording workflow.

Build: tools/oracle-image
Run by the printed immutable image id (not a mutable tag):
  tools/oracle-container sha256:<64-hex-image-id> sh33/options
This checks existing expectations without writing; --write explicitly opts
into recording new ones. No host /usr or package-database mounts, no network,
and a read-only checkout for --check. Run under the lane's CPU/flock policy.
The resulting local image id is build evidence, not a reproducibility promise;
the reproducible inputs are the base digest and all exact package digests.
