{ cmd ? "./rename_documents.py" }:

with import <nixpkgs> { };

let
  pythonPackages = python311Packages;
  project = builtins.baseNameOf ./.;
in
pkgs.mkShell rec {
  name = project;
  buildInputs = [
    pdfgrep
    pythonPackages.python
  ];

  shellHook = ''
    ${cmd}
  '';
}
