# In this .nix file, define a NixOS shell environment with pdfgrep and Python installed

let
  projectName = "docnamer";
  pythonVersion = "311";
  home = builtins.getEnv "HOME";
  venv = "${home}/.virtualenvs/${projectName}";
  pkgs = import <nixos-unstable> {};
  docnamer = pkgs."python${pythonVersion}Packages".buildPythonPackage rec {
    pname = "${projectName}";
    version = "0.0.1";
    format = "flit";
    src = ./.;
  };
  my-python-packages = py: [
    docnamer
    py.flit
  ];
  my-python = pkgs."python${pythonVersion}".withPackages my-python-packages;
in (pkgs.buildFHSUserEnv {
  name = "${projectName}";
  targetPkgs = pkgs: with pkgs; [
    git
    gnupg
    pdfgrep
    my-python
    zsh
  ];
  runScript = "
    rm -f ${venv}
    ln -s ${my-python} ${venv}
    cd ${builtins.toString ./.}
    zsh";
}).env
