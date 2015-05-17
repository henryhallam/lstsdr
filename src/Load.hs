{-# OPTIONS_GHC -Wall #-}

module Load where

import Data.Vector.Storable (Vector)
import qualified Data.Vector.Storable as S
import Foreign.Ptr (castPtr)
import Foreign.ForeignPtr (newForeignPtr_)
import qualified Data.ByteString as B
import Data.ByteString.Unsafe as B (unsafeUseAsCString)

import Data.Bits
import Data.List (foldl')
import Data.Word (Word8)
import Text.Printf

data ScanState = WaitingForCarrier Int
               | FirstEdge Float
               | BitRead Int Float [Bool]
               deriving (Eq, Ord, Show, Read)

samplesPerBit :: Int
samplesPerBit = 104
noDataThreshold :: Float
noDataThreshold = 0.005
dataThreshold :: Float
dataThreshold = 0.01

type Packet = [Bool]

packetToString :: Packet -> String
packetToString = map go
  where
    go False = '0'
    go True = '1'

statemachine :: (ScanState, [Packet]) -> Float -> (ScanState, [Packet])
statemachine (WaitingForCarrier n, pkts) sample
  | n > 6                 = (FirstEdge sample, pkts)
  | sample > dataThreshold = (WaitingForCarrier (n + 1), pkts)
  | otherwise              = (WaitingForCarrier 0, pkts)
statemachine (FirstEdge lastval, pkts) sample
  | signum sample /= signum lastval = (BitRead 1 sample [], pkts)
  | otherwise                       = (FirstEdge sample, pkts)
statemachine (BitRead n acc pkt, pkts) sample
  | n == samplesPerBit =
      if abs acc / fromIntegral n < noDataThreshold
      then (WaitingForCarrier 0, (reverse pkt) : pkts)
      else (BitRead 1 sample ((signum acc > 0) : pkt), pkts)
  | otherwise          = (BitRead (n + 1) (acc + sample) pkt, pkts)

sync :: Word
sync = 0xd391d391

toBytes :: [Bool] -> [Word8]
toBytes bools
  | length top8 < 8 = []
  | otherwise = conv : toBytes (drop 8 bools)
  where
    top8 = take 8 bools
    conv = foldl' (.|.) 0 $
           map (\(b, i) -> if b then bit i else 0) $ zip top8 [7,6..]

bitBools :: (FiniteBits a, Bits a) => a -> [Bool]
bitBools x = reverse $ map (testBit x) [0..finiteBitSize x - 1]

dropTillSync :: [Bool] -> [Bool]
dropTillSync [] = []
dropTillSync pkt
  | take 32 pkt == s = drop 32 pkt
  | otherwise        = dropTillSync $ tail pkt
  where
    s = bitBools sync

process :: Vector Float -> IO ()
process vec =
  putStrLn . unlines .
  -- map (concat . map (printf "%02X ") . toBytes . dropTillSync) . reverse . snd $
  map (concat . map (printf "%c") . toBytes . dropTillSync) . reverse . snd $
  S.foldl' statemachine (WaitingForCarrier 0, []) vec



load :: IO (Vector Float)
load = do
  smpl <- B.readFile "samples.3"
  unsafeUseAsCString smpl $ \cstr -> do
    butts <- newForeignPtr_ $ castPtr cstr
    let len = B.length smpl `div` 4
    return $ S.unsafeFromForeignPtr0 butts len
