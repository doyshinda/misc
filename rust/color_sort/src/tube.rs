use crate::color::*;
use std::cell::RefCell;

const MAX_SIZE: u32 = 4;

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Tube {
    pub colors: RefCell<Vec<ColorBox>>,
    pub tid: u32,
}

impl Tube {
    pub fn new(init_colors: Vec<Color>, tid: u32,) -> Tube {
        let mut colors = Vec::new();
        if init_colors.is_empty() {
            return Tube{
                colors: RefCell::new(colors),
                tid,
            }
        }

        let mut last = ColorBox::new(init_colors[0], 1);
        for c in init_colors.into_iter().skip(1) {
            if c == last.color {
                last.count += 1;
            } else {
                colors.insert(0, last);
                last = ColorBox::new(c, 1);
            }
        }

        colors.insert(0, last);

        Tube{
            colors: RefCell::new(colors),
            tid,
        }
    }

    pub fn is_empty(&self) -> bool {
        self.colors.borrow().is_empty()
    }

    pub fn pop(&self) -> Option<ColorBox> {
        self.colors.borrow_mut().pop()
    }

    pub fn size(&self) -> u32 {
        self.colors.borrow().iter().map(|x| x.count).sum()
    }

    pub fn is_full(&self) -> bool {
        return self.size() == MAX_SIZE
    }

    pub fn push(&self, cb: ColorBox) {
        if self.is_full() {
            panic!("full: {:?}", self.colors);
        }

        if self.is_empty() {
            self.colors.borrow_mut().push(cb);
            return;
        }

        let mut binding = self.colors.borrow_mut();
        let last = binding.last_mut().unwrap();
        if last.count + cb.count > MAX_SIZE {
            panic!("full: {:?} {:?}", self.colors, cb);
        }

        if last.color != cb.color {
            binding.push(cb);
            return;
        }
        last.count += cb.count;
    }

    pub fn solved(&self) -> bool {
        if self.is_empty() {
            return true;
        }

        if !self.is_full() {
            return false;
        }

        self.colors.borrow().windows(2).all(|s| s[0].color == s[1].color)
    }

    pub fn set_colors(&self, colors: RefCell<Vec<ColorBox>>) {
        let mut binding = self.colors.borrow_mut();
        binding.clear();
        binding.append(&mut colors.borrow_mut());
    }

    pub fn fits(&self, other: &ColorBox) -> bool {
        if self.is_full() {
            return false;
        }

        if self.is_empty() {
            return true;
        }

        let size = self.size();
        let mut binding = self.colors.borrow_mut();
        let last = binding.last_mut().unwrap();
        if last.color == other.color {
            return size + other.count <= MAX_SIZE;
        }

        return false;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tube_new_empty() {
        let t = Tube::new(vec![], 1);
        assert_eq!(0, t.size());
        assert!(t.is_empty());
    }

    #[test]
    fn test_tube_new_one_color() {
        let t = Tube::new(vec![Color::Pink], 1);
        assert_eq!(1, t.size());
        assert_eq!(1, t.pop().unwrap().count);
    }

    #[test]
    fn test_tube_new_two_same_color() {
        let t = Tube::new(vec![Color::Red, Color::Red], 1);
        assert_eq!(1, t.colors.borrow().len());
        assert_eq!(2, t.pop().unwrap().count);
    }

    #[test]
    fn test_tube_new_three_color() {
        let t = Tube::new(vec![Color::Red, Color::Red, Color::Blue], 1);
        assert_eq!(2, t.colors.borrow().len());
    }

    #[test]
    fn test_tube_pop() {
        let t = Tube::new(vec![Color::Red, Color::Red, Color::Blue], 1);
        let c = t.pop();
        assert!(c.is_some());
        let c = c.unwrap();
        assert_eq!(2, c.count);
        assert_eq!(Color::Red, c.color);
    }

    #[test]
    fn test_tube_size_full_and_push() {
        let t = Tube::new(vec![Color::Red, Color::Red, Color::Blue], 1);
        t.push(ColorBox::new(Color::Green, 1));
        assert_eq!(3, t.colors.borrow().len());
        assert!(t.is_full());
    }

    #[test]
    fn test_solved() {
        let t = Tube::new(vec![], 1);
        assert!(t.solved());

        t.push(ColorBox::new(Color::LightBlue, 3));
        assert!(!t.solved());
        t.pop();

        t.push(ColorBox::new(Color::LightGreen, 3));
        assert!(!t.solved());

        t.push(ColorBox::new(Color::Pink, 1));
        assert!(!t.solved());
        t.pop();

        t.push(ColorBox::new(Color::LightGreen, 1));
        assert!(t.solved());
    }

    #[test]
    fn test_fits() {
        let t = Tube::new(vec![], 1);
        assert!(t.fits(&ColorBox::new(Color::Purple, 1)));
        t.push(ColorBox::new(Color::Purple, 4));
        assert!(t.is_full());
        assert!(!t.fits(&ColorBox::new(Color::Purple, 1)));

        t.pop();
        t.push(ColorBox::new(Color::Grey, 1));

        assert!(t.fits(&ColorBox::new(Color::Grey, 1)));
        assert!(t.fits(&ColorBox::new(Color::Grey, 2)));
        assert!(t.fits(&ColorBox::new(Color::Grey, 3)));
        assert!(!t.fits(&ColorBox::new(Color::Grey, 4)));
    }

    #[test]
    fn test_set_colors() {
        let t = Tube::new(vec![], 1);
        t.push(ColorBox::new(Color::Purple, 3));

        let c = t.colors.clone();
        t.pop();
        assert!(t.is_empty());

        t.push(ColorBox::new(Color::Grey, 1));
        assert_eq!(1, t.size());

        t.set_colors(c);
        assert_eq!(3, t.size());
        assert_eq!(1, t.colors.borrow().len());
    }
}
