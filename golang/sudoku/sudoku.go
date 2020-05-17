package main

import (
    "fmt"
    "io/ioutil"  
    "strings"
    "sync"
)

const NUMCHARS = 9
type Row [NUMCHARS]uint8
type Board [NUMCHARS]Row
type Slice []uint8

var VALID = Row{1, 2, 3, 4, 5, 6, 7, 8, 9}

func full_row(a Slice) bool {
    if len(a) != NUMCHARS { return false }

    have := make(Slice, 10)
    for _, val := range a { have[val] = 1 }
    for _, val := range VALID { if have[val] == 0 { return false } }
    return true
}

func readBoard() Board {
    data, err := ioutil.ReadFile("board.txt")
    if err != nil {
        fmt.Print("Err opening file: ")
        fmt.Println(err)
    }

    var board Board

    for rdx, line := range strings.Split(string(data), "\n") {
        for cdx, c := range line {
            board[rdx][cdx] = uint8(c) - '0'
        }
    }
    return board
}

func getColValsAtIdx(idx int, board *Board) Slice {
    col := make(Slice, NUMCHARS)
    for row := 0; row < NUMCHARS; row++ {
        col[row] = (*board)[row][idx]
    }
    return col
}

func getSquareVals(ridx int, cidx int, board *Board) Slice {
    squareVals := make(Slice, 0)
    rowStart := (ridx / 3) * 3
    colStart := (cidx / 3) * 3
    for row := rowStart; row < rowStart + 3; row++ {
        for _, col := range (*board)[row][colStart:colStart + 3] {
            squareVals = append(squareVals, col)
        }
    }
    return squareVals
}

var Mux sync.Mutex

func printBoard(board *Board) {
    Mux.Lock()
    defer Mux.Unlock()
    for _, val := range *board {
        for _, col := range val {
            fmt.Print(col)
        }
        fmt.Println()
    }
}

func isSolved(board *Board) bool {
    for _, row := range *board {
        if !full_row(row[:]) { return false }
    }

    for sCol := 0; sCol < 3; sCol++ {
        cidStart := sCol * 3
        cidEnd := cidStart + 3
        for sRow := 0; sRow < 3; sRow++ {
            squareVals := make(Slice, NUMCHARS)
            for row := 0; row < 3; row++ {
                rid := (sRow * 3) + row
                for idx, val := range (*board)[rid][cidStart:cidEnd] {
                    squareVals[row * 3 + idx] = val
                }
            }
            if !full_row(squareVals) { return false }
        } 
    }

    for col := 0; col < NUMCHARS; col++ {
        colVals := getColValsAtIdx(col, board)
        if !full_row(colVals) {
            fmt.Println(colVals)
            return false
        }
    }
    printBoard(board)
    return true
}

func diff(a Slice) Slice {
    have := make(Slice, 10)
    need := make(Slice, 0)
    for _, val := range a { have[uint8(val)] = 1 }
    for _, val := range VALID {
        if have[val] != 1 { need = append(need, val) }
    }
    return need
}

func union(row ...Slice) Slice {
    have := make(Slice, 10)
    need := make(Slice, 0)
    for _, r := range row {
        for _, val := range r { have[val] += 1 }
    }
    leng := uint8(len(row))
    for idx, val := range have {
        if val == leng { need = append(need, uint8(idx)) }
    }
    return need
}

func solve(ridx int, cidx int, board *Board) bool {
    nxtC := cidx + 1
    nxtR := ridx
    if nxtC == NUMCHARS {
        nxtC = 0
        nxtR += 1
    }

    if ridx == NUMCHARS {
        return isSolved(board)
    }
    if (*board)[ridx][cidx] != 0 {
        return solve(nxtR, nxtC, board)
    }

    need := diff((*board)[ridx][:])
    colNeed := diff(getColValsAtIdx(cidx, board))
    SqrNeed := diff(getSquareVals(ridx, cidx, board))
    rem := union(need, colNeed, SqrNeed)
    for _, val := range rem {
        (*board)[ridx][cidx] = val
        switch nxtR {
            case NUMCHARS:
                if isSolved(board) {return true}
            default:
                if solve(nxtR, nxtC, board) {return true}
        }

    }
    (*board)[ridx][cidx] = 0
    return false
}

func solve_parallel(ch chan int, init uint8, board Board) {
    board[0][0] = init
    if solve(0, 1, &board) { ch <- 1 }
}

func main() {
    board := readBoard()
    ch := make(chan int)
    for _, val := range VALID {
        go solve_parallel(ch, val, board)
    }
    <- ch
}
