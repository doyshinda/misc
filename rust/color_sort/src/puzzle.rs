use crate::tube::Tube;
use std::cell::RefCell;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Puzzle {
    pub tubes: RefCell<Vec<Tube>>,
}

impl Puzzle {
    pub fn init(init_tubes: Vec<Tube>) -> Puzzle {
        let mut empty = Vec::new();
        let mut tubes = Vec::new();

        let mut color_count = HashMap::new();
        for t in init_tubes {
            if t.is_empty() {
                empty.push(t);
            } else {
                for c in t.colors.borrow().iter() {
                    let entry = color_count.entry(c.color).or_insert(0);
                    *entry += c.count;
                }
                tubes.push(t);
            }
        }

        for (color, count) in &color_count {
            if (count % 4) != 0 {
                panic!("Mismatched colors: {}: {}", color, count);
            }
        }

        for t in empty {
            tubes.push(t);
        }

        Puzzle{
            tubes: RefCell::new(tubes),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.tubes.borrow().is_empty()
    }

    pub fn solved(&self) -> bool {
        self.tubes.borrow().iter().all(|t| t.solved())
    }
}

mod test {
    #[test]
    fn test_empty() {
        let p = Puzzle::init(vec![]);
        assert_eq!(0, p.tubes.borrow().len());
        assert!(p.solved());
    }

}