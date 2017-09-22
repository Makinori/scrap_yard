module Main where
import Data.IORef
import Graphics.UI.Gtk

showDialog :: Window -> IORef Int -> IO ()
showDialog parent counter = do
  n       <- readIORef counter
  dialog  <- (messageDialogNew
              (Just parent) [] MessageInfo ButtonsOk
              ((show n) ++ " times"))
  print n
  writeIORef counter (n + 1)
  dialogRun dialog
  widgetDestroy dialog

main :: IO ()
main = do
  initGUI
  window <- windowNew
  set window [windowTitle := "Window Title"]
  windowSetDefaultSize window 200 200
  button <- buttonNewWithLabel "click"
  counter<- newIORef 0
  onClicked button (showDialog window counter)
  containerAdd window button
  onDestroy window mainQuit
  widgetShowAll window
  mainGUI
