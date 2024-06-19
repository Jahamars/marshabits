# Mars Habits

Marshabits is a simple habit-tracking application written in Python . The application allows you to add new habits, mark their completion, and view statistics over different periods.

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/jahamars/Marshabits.git
```
```bash
cd marshabits
```

### Step 2: Install dependencies

Make sure you have Python 3 installed. Then install the required libraries:

```bash
pip install urwid
```

### Step 3: Make the script executable and run it:

```bash
chmod +x marshabits.sh
```
```bash
sudo ./marshabits.sh
```

## Usage

After installation, you can run the application using the `marshabits` command in the terminal:

```bash
marshabits
```
![marshabits](https://photos.app.goo.gl/nVbDGpuGXLBXwh2d6)

## Shortcuts
Here is a list of all the shortcuts for the program:

1. **Main Menu**:
   - **1** or **a**: Add a new habit.
   - **2** or **d**: Display habits.
   - **3** or **p**: Plot habits.
   - **4** or **m**: Mark habits as done.
   - **5** or **x**: Delete a habit.
   - **6** or **t**: Manage Trash Bin.
   - **7** or **q/Q**: Quit the program.

2. **Global Shortcuts**:
   - **b**: Go back to the previous menu or view.
   - **Ctrl+C** (on terminal/command prompt): Quit the program.

## Deletion

```bash
find . -type d \( -name "marshabits" -o -name "habits_json" -o -name "trash_bin" \) -exec rm -r {} +
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

# Come back for new updates

