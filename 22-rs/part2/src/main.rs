#![allow(dead_code)]
#![allow(unreachable_code)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_variables)]

use clap::Parser;
use combination::*;
use console::style;
use either::Either;
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressFinish, ProgressStyle};
use num::integer::gcd;
use primal;
use rand::seq::SliceRandom;
use rand::thread_rng;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet};
use std::fs;
use tabled::{
    object::{Rows, Segment},
    Alignment, MaxWidth, Modify, Style, Table, Tabled,
};
static DIRS: [(i32, i32); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];
static RIGHT: usize = 0;
static DOWN: usize = 1;
static LEFT: usize = 2;
static UP: usize = 3;

#[derive(Parser, Debug)]
struct Blueprint {
    #[clap(long, default_value_t = 1)]
    id: u32,
    #[clap(short, long, default_value_t = 1)]
    ore_robot_cost: u32,
    #[clap(short, long, default_value_t = 1)]
    clay_robot_cost: u32,
    #[clap(short = 'b', long)]
    obsidian_robot_cost: Vec<u32>,
    #[clap(short, long)]
    geode_robot_cost: Vec<u32>,
}
#[derive(Parser, Debug)]
struct Cli {
    #[clap(short, long, default_value_t = String::from("ex.in"))]
    input_file: String,
}

type Grid = Vec<Vec<char>>;
type Cube = HashMap<usize, Grid>;

#[derive(Debug)]
struct Point {
    i: u32,
    j: u32,
    side: u32,
    dir_id: usize,
}

fn display_grid(grid: &Grid) {
    grid.iter().for_each(|line| {
        for c in line {
            print!("{}", c);
        }
        println!();
    });
    println!();
}

fn starting_point(grid: &Vec<&str>) -> (usize, usize) {
    let j = grid[0].chars().take_while(|c| *c == ' ').count();

    (0, j)
}

fn next(cube: &Cube, p: &Point) -> Point {
    let delta = DIRS[p.dir_id];
    let n = cube.get(&1).unwrap().len() as i32;

    let mut q = ((p.i as i32 + delta.0), (p.j as i32 + delta.1));

    if 0 <= q.0 && q.0 < n && 0 <= q.1 && q.1 < n {
        return Point {
            side: p.side,
            i: q.0 as u32,
            j: q.1 as u32,
            dir_id: p.dir_id,
        };
    }

    let n = n as u32;

    if p.side == 1 {
        if p.dir_id == RIGHT { return Point { side: 2, i: p.i,      j: 0,     dir_id: RIGHT}; }
        if p.dir_id == LEFT  { return Point { side: 4, i: n-p.i-1,  j: 0,     dir_id: RIGHT}; }
        if p.dir_id == UP    { return Point { side: 6, i: p.j,      j: 0,     dir_id: RIGHT}; }
        if p.dir_id == DOWN  { return Point { side: 3, i: 0,        j: p.j,   dir_id: DOWN}; }
    }
    if p.side == 2 {
        if p.dir_id == RIGHT { return Point { side: 5, i: n-p.i-1,  j: n-1,   dir_id: LEFT}; }
        if p.dir_id == LEFT  { return Point { side: 1, i: p.i,      j: n-1,   dir_id: LEFT}; }
        if p.dir_id == UP    { return Point { side: 6, i: n-1,      j: p.j,   dir_id: UP}; }
        if p.dir_id == DOWN  { return Point { side: 3, i: p.j,      j: n-1,   dir_id: LEFT}; }
    }
    if p.side == 3 {
        if p.dir_id == RIGHT { return Point { side: 2, i: n-1,      j: p.i,   dir_id: UP}; }
        if p.dir_id == LEFT  { return Point { side: 4, i: 0,        j: p.i,   dir_id: DOWN}; }
        if p.dir_id == UP    { return Point { side: 1, i: n-1,      j: p.j,   dir_id: UP}; }
        if p.dir_id == DOWN  { return Point { side: 5, i: 0,        j: p.j,   dir_id: DOWN}; }
    }
    if p.side == 4 {
        if p.dir_id == RIGHT { return Point { side: 5, i: p.i,      j: 0,     dir_id: RIGHT}; }
        if p.dir_id == LEFT  { return Point { side: 1, i: n-p.i-1,  j: 0,     dir_id: RIGHT}; }
        if p.dir_id == UP    { return Point { side: 3, i: p.j,      j: 0,     dir_id: RIGHT}; }
        if p.dir_id == DOWN  { return Point { side: 6, i: 0,        j: p.j,   dir_id: DOWN}; }
    }
    if p.side == 5 {
        if p.dir_id == RIGHT { return Point { side: 2, i: n-p.i-1,  j: n-1,   dir_id: LEFT}; }
        if p.dir_id == LEFT  { return Point { side: 4, i: p.i,      j: n-1,   dir_id: LEFT}; }
        if p.dir_id == UP    { return Point { side: 3, i: n-1,      j: p.j,   dir_id: UP}; }
        if p.dir_id == DOWN  { return Point { side: 6, i: p.j,      j: n-1,   dir_id: LEFT}; }
    }
    if p.side == 6 {
        if p.dir_id == RIGHT { return Point { side: 5, i: n-1,      j: p.i,   dir_id: UP}; }
        if p.dir_id == LEFT  { return Point { side: 1, i: 0,        j: p.i,   dir_id: DOWN}; }
        if p.dir_id == UP    { return Point { side: 4, i: n-1,      j: p.j,   dir_id: UP}; }
        if p.dir_id == DOWN  { return Point { side: 2, i: 0,        j: p.j,   dir_id: DOWN}; }
    }

    Point {
        side: 1,
        i: 1,
        j: 1,
        dir_id: 1,
    }
}

fn get_ops(s: &str) -> Vec<Either<char, usize>> {
    let mut ops: Vec<Either<char, usize>> = Vec::new();
    let mut x = 0;
    for c in s.chars() {
        if c == 'L' || c == 'R' {
            if x != 0 {
                ops.push(Either::Right(x));
            }
            ops.push(Either::Left(c));
            x = 0;
        } else {
            x = x * 10 + c.to_digit(10).unwrap() as usize;
        }
    }
    if x != 0 {
        ops.push(Either::Right(x));
    }
    ops
}

fn explore(cube: &Cube, p: &mut Point, ops: &Vec<Either<char, usize>>) -> usize {
    let n = cube.get(&1).unwrap().len() as u32;
    for op in ops {
        if op == &Either::Left('L') {
            p.dir_id = (p.dir_id + 4 - 1) % 4;
        }
        if op == &Either::Left('R') {
            p.dir_id = (p.dir_id + 1) % 4;
        }

        if let &Either::Right(steps) = op {
            for _ in 0..steps {
                let q = next(cube, p);

                if q.i >= 50 || q.j>=50 {
                    panic!("Generated next({:?}) == {:?} which is bad", p, q);
                }

                if cube.get(&(q.side as usize)).unwrap()[q.i as usize][q.j as usize] == '#' {
                    break;
                } else {
                    *p = q;
                }
            }
        }
    }
    println!("Arrived at {:?}", p);

    // Generate initial grid positions based on individual sides
    if p.side == 1 {             p.j += n;   }
    if p.side == 2 {             p.j += 2*n; }
    if p.side == 3 { p.i += n;   p.j += n;   }
    if p.side == 4 { p.i += 2*n;             }
    if p.side == 5 { p.i += 2*n; p.j += n;   }
    if p.side == 6 { p.i += 3*n;             }

    ((p.i + 1) * 1000 + (p.j + 1) * 4 + (p.dir_id as u32)) as usize
}

fn main() {
    let args = Cli::parse();

    let mut cube: Cube = HashMap::new();

    for side in 1..7 {
        let contents = fs::read_to_string(format!("{}", side))
            .expect("Should have been able to read the file");
        let lines: Vec<&str> = contents.trim().split('\n').collect();
        let lc = lines.len();
        let grid: Vec<Vec<char>> = lines.into_iter().map(|l| l.trim().chars().collect()).collect();
        assert!(grid.len() == 50);
        assert!(grid[0].len() == 50);
        display_grid(&grid);

        cube.insert(side, grid);
    }
    let ops_s = fs::read_to_string("ops")
        .expect("Should have been able to read the file");
    let ops = get_ops(&ops_s.trim());

    let mut p = Point{side: 1, i: 0, j: 0, dir_id: RIGHT};
    println!("Starting point: {:?}", p);

    let ans = explore(&cube, &mut p, &ops);
    println!("Answer is {}", style(ans).red());
}

// 36182 to low
