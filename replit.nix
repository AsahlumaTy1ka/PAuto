{pkgs}: {
  deps = [
    pkgs.c-ares
    pkgs.rustc
    pkgs.openssl
    pkgs.libiconv
    pkgs.cargo
    pkgs.pkg-config
    pkgs.libffi
    pkgs.cacert
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.grpc
    pkgs.glibcLocales
    pkgs.dbus
  ];
}
