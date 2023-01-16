with (import <nixpkgs> {});
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.5.0";  # update this version
  }) {
    #python = "python310";
  };
  pyEnv = mach-nix.mkPython rec {
    requirements = builtins.readFile ./requirements.txt;
    # providers.shapely = "sdist,nixpkgs";
  };
in
mach-nix.nixpkgs.mkShell {
  buildInputs = [
    wget
	pyEnv
	python3Packages.python-lsp-server
  ];
}
