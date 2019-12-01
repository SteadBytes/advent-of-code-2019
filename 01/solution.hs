module Day01 (partOne, partTwo) where

masses = map (read :: String -> Int) . lines
calcFuel = subtract 2 . (`div` 3)
fuelFuels = takeWhile (> 0) . iterate calcFuel . calcFuel

partOne = sum . map calcFuel
partTwo = sum . concatMap fuelFuels

main :: IO()
main = do
    contents <- readFile "input.txt"
    putStrLn $ "Part 1: " ++ show (partOne (masses contents))
    putStrLn $ "Part 2: " ++ show (partTwo (masses contents))
