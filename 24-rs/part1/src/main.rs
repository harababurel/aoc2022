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

#[derive(Parser, Debug)]
struct Cli {
    #[clap(short, long, default_value_t = String::from("ex.in"))]
    input_file: String,
}

#[derive(Eq, PartialEq, Hash)]
enum Direction {
    LEFT,
    RIGHT,
    UP,
    DOWN,
    NONE,
}
struct Map {
    grid: Vec<Vec<char>>,
    blizzards: HashMap<Direction, Vec<(usize, usize)>>,
}

impl Map {
    fn from_grid(grid: Vec<Vec<char>>) -> Self {
        let mut blizzards: HashMap<Direction, Vec<(usize, usize)>> = HashMap::from([
            (Direction::LEFT, Vec::new()),
            (Direction::RIGHT, Vec::new()),
            (Direction::UP, Vec::new()),
            (Direction::DOWN, Vec::new()),
        ]);

        for i in 0..grid.len() {
            for j in 0..grid[i].len() {
                let d = match grid[i][j] {
                    '>' => Direction::RIGHT,
                    '<' => Direction::LEFT,
                    'v' => Direction::DOWN,
                    '^' => Direction::UP,
                    _ => Direction::NONE,
                };

                if d != Direction::NONE {
                    blizzards
                        .get_mut(&d)
                        .get_or_insert(&mut Vec::new())
                        .push((i, j));
                }
            }
        }

        Map { grid, blizzards }
    }
    fn cell_free(&self, cell: (usize, usize), t: usize) -> bool {
        for (d, bs) in self.blizzards.iter() {
            for b in bs {
                let (mut ni, mut nj) = b;

                match d {
                    Direction::RIGHT => {
                        nj = ((nj - 1) + t) % (self.cols() - 2) + 1;
                    }
                    Direction::LEFT => {
                        nj = ((nj - 1) - t + 10000 * (self.cols() - 2)) % (self.cols() - 2) + 1;
                    }
                    Direction::UP => {
                        ni = ((ni - 1) - t + 10000 * (self.lines() - 2)) % (self.lines() - 2) + 1;
                    }
                    Direction::DOWN => {
                        ni = ((ni - 1) + t) % (self.lines() - 2) + 1;
                    }
                    _ => {
                        panic!("This should never happen");
                    }
                };
                if (ni, nj) == cell {
                    return false;
                }
            }
        }

        true
    }
    fn lines(&self) -> usize {
        self.grid.len()
    }
    fn cols(&self) -> usize {
        self.grid[0].len()
    }
    fn display_accessibility(&self, t: usize) {
        println!("Accessibility at time {}:", t);
        for i in 0..self.lines() {
            for j in 0..self.cols() {
                if i == 0 || i == self.lines() - 1 || j == 0 || j == self.cols() - 1 {
                    print!("{}", self.grid[i][j]);
                    continue;
                }
                if self.cell_free((i, j), t) {
                    print!(".");
                } else {
                    print!("*");
                }
            }
            println!();
        }
        println!();
    }
}

fn display_grid(grid: &Vec<Vec<char>>) {
    grid.iter().for_each(|line| {
        line.iter().for_each(|c| {
            print!("{}", c);
        });
        println!();
    });
    println!();
}

fn solve(m: &Map) -> usize {
    let mut accessible: HashSet<(usize, usize, usize)> = HashSet::new();
    // accessible[(t, i, j)]: cell (i, j) is accessible at time t

    let source = (0, 1);
    let target = (m.lines() - 1, m.cols() - 2);

    accessible.insert((0, source.0, source.1));
    let dirs: [(i32, i32); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];

    for t in 1.. {
        for i in 0..m.lines() {
            for j in 0..m.cols() {
                if accessible.contains(&(t - 1, i, j)) && m.cell_free((i, j), t) {
                    accessible.insert((t, i, j));
                }

                if m.grid[i][j] == '#' || !m.cell_free((i, j), t) {
                    continue;
                }

                for (di, dj) in dirs {
                    let (pi, pj) = (i as i32 + di, j as i32 + dj);
                    if pi < 0 || pi >= m.lines() as i32 || pj < 0 || pj >= m.cols() as i32 {
                        continue;
                    }
                    let (pi, pj) = (pi as usize, pj as usize);

                    if accessible.contains(&(t - 1, pi, pj)) {
                        accessible.insert((t, i, j));
                        break;
                    }
                }
            }
        }
        if accessible.contains(&(t, target.0, target.1)) {
            println!("Can reach target at time {}", t);
            return t;
        }
    }
    0
}

fn main() {
    let args = Cli::parse();

    let contents =
        fs::read_to_string(args.input_file).expect("Should have been able to read the file");

    let lines: Vec<&str> = contents.trim().split('\n').collect();
    println!("lines: {:?}", lines);
    let grid: Vec<Vec<char>> = lines
        .into_iter()
        .map(|line| line.chars().clone().collect())
        .collect();

    display_grid(&grid);

    let m = Map::from_grid(grid);

    println!(
        "There are {} blizzards",
        m.blizzards.iter().map(|(k, v)| v.len()).sum::<usize>()
    );

    let ans = solve(&m);
    println!("Answer is {}", style(ans).red());
}
