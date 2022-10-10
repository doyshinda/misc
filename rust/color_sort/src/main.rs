mod color;
mod tube;
mod puzzle;

use color::Color;
use puzzle::Puzzle;
use tube::Tube;
use std::cell::RefCell;

#[derive(Debug)]
struct SolveInput{
    puz: Puzzle,
    solved: RefCell<bool>,
    c: RefCell<u32>,
    path: RefCell<Vec<(u32, u32)>>,
}

impl SolveInput {
    fn push(&self, val: (u32, u32)) {
        self.path.borrow_mut().push(val)
    }

    fn pop(&self) {
        self.path.borrow_mut().pop();
    }

    fn inc(&self) {
        let mut c = self.c.borrow_mut();
        *c += 1;
    }

    fn dec(&self) {
        let mut c = self.c.borrow_mut();
        *c -= 1;
    }

    fn set_solved(&self, val: bool) {
        let mut s = self.solved.borrow_mut();
        *s = val;
    }

    fn solved(&self) -> bool {
        let resp = self.solved.borrow();
        *resp
    }
}

fn solve(si: &SolveInput) {
    if *si.c.borrow() == 0 {
        panic!("Exhausted tries");
    }

    if si.puz.is_empty() {
        si.set_solved(false);
        return;
    }

    if si.puz.solved() {
        si.set_solved(true);
        return;
    }

    let upper_binding = si.puz.tubes.borrow();
    for curr_tube in upper_binding.iter() {
        if curr_tube.is_empty() {
            continue;
        }

        let curr_color = curr_tube.pop().unwrap();
        for candidate in upper_binding.iter() {
            if candidate.tid == curr_tube.tid {
                continue;
            }

            if candidate.is_empty() && curr_tube.is_empty() {
                continue;
            }

            if candidate.fits(&curr_color) {
                let candidate_colrs = candidate.colors.clone();
                candidate.push(curr_color.clone());
                si.push((curr_tube.tid, candidate.tid));
                si.dec();
                
                solve(si);
                if si.solved() {
                    return;
                }
                si.inc();
                candidate.set_colors(candidate_colrs);
                si.pop();
            }
        }
        curr_tube.push(curr_color);
    }
}

fn main() {
    let teal = Color::Teal;
    let fusia = Color::Fusia;
    let lg = Color::LightGreen;
    let lblue = Color::LightBlue;
    let pink = Color::Pink;
    let grey = Color::Grey;
    let blue = Color::Blue;
    let red = Color::Red;
    let orange = Color::Orange;
    let purple = Color::Purple;
    let green = Color::Green;
    let yellow = Color::Yellow;
    let tubes = vec![
        Tube::new(vec![teal, blue, blue, purple], 1),
        Tube::new(vec![blue, purple, grey, fusia], 2),
        Tube::new(vec![grey, purple, pink, pink], 3),
        Tube::new(vec![green, orange, pink, lblue], 4),
        Tube::new(vec![lblue, fusia, green, yellow], 5),
        Tube::new(vec![lg, lg, lblue, yellow], 6),
        Tube::new(vec![purple, blue, yellow, green], 7),
        Tube::new(vec![red, orange, teal, yellow], 8),
        Tube::new(vec![lg, grey, orange, teal], 9),
        Tube::new(vec![pink, fusia, fusia, teal], 10),
        Tube::new(vec![red, red, lg, lblue], 11),
        Tube::new(vec![grey, orange, red, green], 12),
        Tube::new(vec![], 13),
        Tube::new(vec![], 14),
    ];
    let p = Puzzle::init(tubes);
    let si = SolveInput{
        solved: RefCell::new(false),
        c: RefCell::new(200),
        puz: p,
        path: RefCell::new(vec![]),
    };

    solve(&si);
    if si.solved() {
        for p in &*si.path.borrow() {
            println!("{:0>2} -> {:0>2}", p.0, p.1);
        }
    } else {
        println!("FAILED");
    }
}
