{-# LANGUAGE CPP #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
{-# OPTIONS_GHC -fno-warn-implicit-prelude #-}
module Paths_gui_test (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/bin"
libdir     = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/lib/x86_64-linux-ghc-8.0.2/gui-test-0.1.0.0"
dynlibdir  = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/lib/x86_64-linux-ghc-8.0.2"
datadir    = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/share/x86_64-linux-ghc-8.0.2/gui-test-0.1.0.0"
libexecdir = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/libexec"
sysconfdir = "/home/makinori/program/haskell/gui-test/.stack-work/install/x86_64-linux/lts-8.18/8.0.2/etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "gui_test_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "gui_test_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "gui_test_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "gui_test_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "gui_test_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "gui_test_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
