with (import <nixpkgs> {});
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.5.0";
  }) {
  };
  pyEnv = mach-nix.mkPython rec {
    requirements = builtins.readFile ./requirements.txt;
  };
in



mach-nix.nixpkgs.mkShell {
  buildInputs = [
     wget
     pyEnv
  ];

  shellHook = ''
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
    sh setup.sh
  '';
}
