use clap::Parser;
use console::style;
use rand::rngs::ThreadRng;
use rand::Rng;
use std::collections::HashMap;

fn explore(
    args: &Cli,
    rng: &mut ThreadRng,
    bp: &Blueprint,
    best: &mut u32,
    robots: (u32, u32, u32, u32),
    resources: (u32, u32, u32, u32),
    history: String,
    t: u32,
) -> u32 {
    let (or, cr, br, gr) = robots;
    let (o, c, b, g) = resources;
    if t == args.tmax {
        if &g > best {
            println!("Found new best: {} via\n{}", g, history);
            *best = g;
        }
        return g;
    }

    let mut ret = 0;

    let gc = &bp.geode_robot_cost;
    let bc = &bp.obsidian_robot_cost;
    let cc = &bp.clay_robot_cost;
    let oc = &bp.ore_robot_cost;

    let mut should_buy_g = o >= gc[0] && b >= gc[1] && rng.gen::<f32>() <= args.pg;
    let mut should_buy_b = t + 1 < args.tmax && o >= bc[0] && c >= bc[1] && rng.gen::<f32>() <= args.pb;
    let mut should_buy_c = t + 1 < args.tmax && o >= *cc && rng.gen::<f32>() <= args.pc;
    let mut should_buy_o = t + 1 < args.tmax && o >= *oc && rng.gen::<f32>() <= args.po;

    // don't buy a robot if it could have been bought last round but wasn't
    if history.ends_with('.') {
        if (o-or) >= *oc {
            should_buy_o = false;
        }
        if (o-or) >= *cc {
            should_buy_c = false;
        }
        if (o-or) >= bc[0] && (c-cr) >= bc[1] {
            should_buy_b = false;
        }
        if (o-or) >= gc[0] && (b-br) >= gc[1] {
            should_buy_g = false;
        }
    }

    ret = std::cmp::max(ret, explore(args,rng,bp,best,(or, cr, br, gr),(o + or, c + cr, b + br, g + gr),format!("{}.", history),t + 1));
    if should_buy_g { ret = std::cmp::max(ret, explore(args,rng,bp,best,(or, cr, br, gr + 1),(o + or - gc[0], c + cr, b + br - gc[1], g + gr),format!("{}g", history),t + 1)); }
    if should_buy_b { ret = std::cmp::max(ret, explore(args,rng,bp,best,(or, cr, br + 1, gr),(o + or - bc[0], c + cr - bc[1], b + br, g + gr),format!("{}b", history),t + 1)); }
    if should_buy_c { ret = std::cmp::max(ret, explore(args,rng,bp,best,(or, cr + 1, br, gr),(o + or - cc, c + cr, b + br, g + gr),format!("{}c", history),t + 1)); }
    if should_buy_o { ret = std::cmp::max(ret, explore(args,rng,bp,best,(or + 1, cr, br, gr),(o + or - oc, c + cr, b + br, g + gr),format!("{}o", history),t + 1)); }

    ret
}

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
    #[clap(short, long, default_value_t = 1)]
    blueprint: u32,
    #[clap(short, long, default_value_t = 32)]
    tmax: u32,
    #[clap(long, default_value_t = 1.0)]
    po: f32,
    #[clap(long, default_value_t = 1.0)]
    pc: f32,
    #[clap(long, default_value_t = 1.0)]
    pb: f32,
    #[clap(long, default_value_t = 1.0)]
    pg: f32,
}

fn main() {
    let args = Cli::parse();

    let tests = HashMap::from([
        (
            1,
            Blueprint {
                id: 1,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 13],
                geode_robot_cost: vec![3, 7],
            },
        ),
        (
            2,
            Blueprint {
                id: 2,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 20],
                geode_robot_cost: vec![2, 12],
            },
        ),
        (
            3,
            Blueprint {
                id: 3,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 9],
                geode_robot_cost: vec![3, 7],
            },
        ),
    ]);

    let blueprint = tests.get(&args.blueprint).expect("Blueprint not found");

    let mut rng = rand::thread_rng();
    let mut best = 0;

    println!("Running with config: {:#?}", args);

    let ans = explore(
        &args,
        &mut rng,
        blueprint,
        &mut best,
        (1, 0, 0, 0),
        (0, 0, 0, 0),
        String::new(),
        0,
    );
    println!(
        "Answer for blueprint {} is {}",
        blueprint.id,
        style(ans).red()
    );
}
