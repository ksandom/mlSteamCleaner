#!/usr/bin/env python3
"""Prep a CSV file for usage.
Now that we are working with smaller files, we can just do everything in memory. """

import sys
import csv
import math
import matplotlib.pyplot as plt

# Parameters from the command line.
name = sys.argv[1]
file_name = sys.argv[2]
sample_size = int(sys.argv[3])
sample_size_fit = sample_size - 1
destination = sys.argv[4]
destination_graph_image = sys.argv[5]
destination_graph_pdf = sys.argv[6]
destination_samples_binary = sys.argv[7]
destination_samples_clean = sys.argv[8]
destination_samples_dirty = sys.argv[9]
destination_samples_graph_clean = sys.argv[10]
destination_samples_graph_dirty = sys.argv[11]

# Moving mean size.
mean_size = 20

# Threshold for when a change is considered to be an error.
threshold = 0.0007
n_threshold_value = threshold * -1
angle_threshold = 1
n_angle_threshold = angle_threshold * -1

# Create the float graph. - Useful for pre-transform debugging.
create_float_graph = False

# Create the centered int graph.
create_centered_graph = False

# Create the signed int graph.
create_signed_graph = False

# Create the normalised angles graph.
create_normalised_angles_graph = False


# Create a graph for every sample. EXTREMELY slow.
create_sample_graphs = False

# Where to save various stuff.
destination_file = destination + "/" + name + ".csv"
destination_graph_file_image = destination_graph_image + "/" + name
destination_graph_file_pdf = destination_graph_pdf + "/" + name

# Which fields to put into the sample files.
fields_to_take = [
    'long',
    'lat',
    'correctedLong',
    'correctedLat',
    'angleDiffInt',
    'angleDiffIntPositiveCentered',
    'correctedAngleDiffInt',
    'correctedAngleDiffIntPositiveCentered',
    'diffScaledInt',
    'correctedDiffScaledInt',
    'diff',
    'angleDiffDiff',
    'angleDiff',
    'angle']

# What percentage of samples to put in A.
ab_split = 0.8
ab_split_negative = 1 - ab_split

# Which fields to put into the combined binary samples file.
combined_binary_fields_to_take = [
    # 'long',
    # 'lat',
    # 'correctedLong',
    # 'correctedLat',
    'angleDiffIntPositiveCentered',
    'diffScaledInt',
    'correctedAngleDiffIntPositiveCentered',
    'correctedDiffScaledInt'
    ]

# # Which fields to put into the combined samples file.
combined_angle_fields_to_take = [
    'angleDiffDiff'
    ]

# Re-scaling the angle data to make stronger signals for easier training.
# cutOff = 80
# nCutOff = cutOff * -1
unScaled = 0.1
nUnScaled = unScaled * -1

# Input angle data OOB cutoff. This is for filtering out data that is going to give us problems.
angleCutoff = 0.98
nAngleCutoff = 0.02

# Some loose maths stuff.
pi = math.pi
half_pi = pi/2

# Scale the angle values. This is effectively the base from which the signal is scaled. Making the number smaller (ie diving pi by a larger number) increases the gain.
angle_base = pi / 800

# pylint: disable=C0301
# Variables being incorrectly identified as constants. Ultimately, there's too much code in the root. I'm not going to invest time into this for now. But it would be worth doing at some point.
# pylint: disable=C0103


def read_csv(in_file_name):
    """ Read the origin file. """

    rows = []
    with open(in_file_name, newline='', encoding="utf-8") as csvfileIn:
        reader = csv.DictReader(csvfileIn)

        for row in reader:
            shouldSkip = False

            if not row.get('long'):
                shouldSkip = True
            if not row.get('lat'):
                shouldSkip = True

            if shouldSkip:
                print ("Skipping row that is missing data.")
                continue

            rows.append(row)

            # print(row['default_latitude-deg'], row['default_longitude-deg'])
            # keep = {'long': row['default_longitude-deg'], 'lat': row['default_latitude-deg']}

    sub_row_count = len(rows)
    if sub_row_count < 3:
        print("Not enough rows to continue with " + name)
        sys.exit()

    return rows

def write_csv(out_file_name, rows):
    """ Write the destination file. """

    if len(rows) < 2:
        print("No rows for " + out_file_name + ". Skipping.")
        return

    with open(out_file_name, 'w', newline='', encoding="utf-8") as csv_file_out:
        writer = csv.DictWriter(csv_file_out, fieldnames=rows[1].keys())
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

def calculate_diff(rows, long_field, lat_field, out_field_distance, out_field_angle):
    """ Calculate diff. """

    for index, row in enumerate(rows):
        if index == 0:
            row[out_field_distance] = 0
            row[out_field_angle] = 0
            row[out_field_angle + 'Diff'] = 0
            continue

        long_diff = float(row[long_field]) - float(rows[index - 1][long_field])
        lat_diff = float(row[lat_field]) - float(rows[index - 1][lat_field])

        row[out_field_distance] = (long_diff**2 + lat_diff**2)**0.5

        previousAngle = rows[index - 1][out_field_angle]
        row[out_field_angle] = math.atan2(lat_diff, long_diff)
        row[out_field_angle + 'Diff'] = row[out_field_angle] - previousAngle

        if row[out_field_angle + 'Diff'] > half_pi:
            row[out_field_angle + 'Diff'] -= pi
        if row[out_field_angle + 'Diff'] < half_pi * -1:
            row[out_field_angle + 'Diff'] += pi

        # print(row[out_field_angle], previousAngle, row[out_field_angle + 'Diff'])

    return rows

def calculate_mean(rows, in_field, out_field):
    """ Calculate mean. """

    for index, row in enumerate(rows):
        if index == 0:
            row[out_field] = 0
            continue

        half_mean_size = round(mean_size / 2)
        mean_start = index - half_mean_size
        mean_stop = index + half_mean_size

        # Protect bounds.
        mean_start = max(mean_start, 1)
        mean_stop = min(mean_stop, row_count)

        actual_mean_size = mean_stop - mean_start
        mean_sum = 0

        for meanPos in range(mean_start, mean_stop):
            mean_sum += rows[meanPos][in_field]

        row[out_field] = mean_sum / actual_mean_size

    return rows


def calculate_simple_diff(rows, in_field, out_field):
    """ Calculate diffdiff. """

    for index, row in enumerate(rows):
        if index == 0:
            row[out_field] = 0
            continue

        row[out_field] = row[in_field] - rows[index - 1][in_field]

    return rows

def to_int_degrees(rows, in_field, out_field, inScale, out_scale):
    """ Make an integer version of an angle that is easier to parse for ML purposes. """

    n_out_scale = out_scale * -1

    for _, row in enumerate(rows):
        row[out_field + 'DegreesDebug'] = math.degrees(row[in_field])
        row[out_field] = int(row[out_field + 'DegreesDebug'] / inScale * out_scale)

        if row[out_field] > out_scale:
            row[out_field] = out_scale

        if row[out_field] < n_out_scale:
            row[out_field] = n_out_scale

        n_key = out_field + "N"
        row[n_key] = row[out_field] * -1

         # Expected fields to be used.
        row[out_field + 'PositiveCentered'] = row[out_field] + out_scale
        row[out_field + 'PositiveCenteredN'] = row[n_key] + out_scale

    return rows

def to_int_distance(rows, in_field, out_field, inScale, out_scale):
    """ Make an integer version of a distance that is easier to parse for ML purposes. """

    n_out_scale = out_scale * -1

    for _, row in enumerate(rows):
        row[out_field] = int(row[in_field] / inScale * out_scale)

        if row[out_field] > out_scale:
            row[out_field] = out_scale

        if row[out_field] < n_out_scale:
            row[out_field] = n_out_scale

        row[out_field + "N"] = row[out_field] * -1

        row[out_field + 'Centered'] = row[out_field] + out_scale
        row[out_field + 'CenteredN'] = row[out_field + "N"] + out_scale

    return rows


# "Too many branches". In this case, it would make it less readable to split it out.
# pylint: disable=R0912

# TODO Refactor this function.
# pylint: disable=R0914
# pylint: disable=R0913

def create_generic_graph(out_file_image, out_file_pdf, graph_name, y1_label, y1_fields, y2_label, y2_fields, rows, sub_threshold_value = 0, create_pdf = True):
    """ Dynamically generate a graph. """

    y1_field_values = {}
    y2_field_values = {}

    sub_n_threshold_value = sub_threshold_value * -1

    for row_index, row1 in enumerate(rows):
        if row_index == 0:
            x = []
            pThreshold = []
            nThreshold = []

            for _, field in enumerate(y1_fields):
                y1_field_values[field] = []

            for _, field in enumerate(y2_fields):
                y2_field_values[field] = []

        x.append(row_index)

        for _, field in enumerate(y1_fields):
            y1_field_values[field].append(row1[field])

        for _, field in enumerate(y2_fields):
            y2_field_values[field].append(row1[field])

        if sub_threshold_value:
            pThreshold.append(sub_threshold_value)
            nThreshold.append(sub_n_threshold_value)

    fig, ax1 = plt.subplots()

    # Primary y-axis.
    line_width = 0.5
    ax1.set_xlabel('Rows')
    ax1.set_ylabel(y1_label)

    if sub_threshold_value:
        ax1.plot(x, pThreshold, linewidth = line_width, label="pThreshold")
        ax1.plot(x, nThreshold, linewidth = line_width, label="nThreshold")

    for _, field in enumerate(y1_fields):
        ax1.plot(x, y1_field_values[field], linewidth = line_width, label=field)

    # Secondary y-axis.
    if len(y2_fields):
        ax2 = ax1.twinx()
        ax2.set_ylabel(y2_label)

        for _, field in enumerate(y2_fields):
            ax2.plot(x, y2_field_values[field], linewidth = line_width, label=field)

    plt.title(graph_name)

    fig.tight_layout()

    ax1.legend(loc=0)

    if len(y2_fields):
        ax2.legend(loc=1)

    plt.savefig(out_file_image + '.png', bbox_inches='tight', dpi=600)

    if create_pdf:
        plt.savefig(out_file_pdf + '.pdf', bbox_inches='tight')
    # plt.show()

    plt.close()

def number_to_binary(number):
    return str(bin(number))[2:].rjust(8, '0')[-8:]

def rows_to_binary_row(rows, which_fields_to_take, good):
    combined_row = {}

    # These first two loops could be swapped. I've put them this way around in the hopes that
    # the bits of a field will be put together in the final CSV.
    for _, field_name in enumerate(which_fields_to_take):
        for index, row in enumerate(rows):
            bits = number_to_binary(row[field_name])

            for pos in range(0, 8):
                final_field_name = field_name + '_' + str(index) + '_' + str(pos)
                combined_row[final_field_name] = bits[pos:pos + 1]

                if combined_row[final_field_name] == 'b':
                    print("There's an error in the data. Negative values?")
                    print(bits)
                    print(index)
                    print(pos)
                    print(final_field_name)
                    print(row[field_name])
                    sys.exit(1)

    good_value = 0
    if (good): good_value = 1
    combined_row['good'] = good_value

    return combined_row

def rows_to_angle_row(rows, which_fields_to_take):
    combined_row = {}

    for _, field_name in enumerate(which_fields_to_take):
        for index, row in enumerate(rows):
            final_field_name = field_name + '_' + str(index)
            combined_row[final_field_name] = row[field_name]

    return combined_row

def rows_to_angle_row_scale(rows, which_fields_to_take, scale_from, offset=0, answer_value=False):
    combined_row = {}

    for _, field_name in enumerate(which_fields_to_take):
        for index in range(0, len(rows)-1):
            final_field_name = field_name + '_' + str(index)
            combined_row[final_field_name] = rows[index][field_name]

            combined_row[final_field_name] = ((combined_row[final_field_name] + offset) / (scale_from * 2))

            if combined_row[final_field_name] > 1:
                combined_row[final_field_name] = 1

            if combined_row[final_field_name] < 0:
                combined_row[final_field_name] = 0

            combined_row[final_field_name] = round(combined_row[final_field_name], 3)

            #print(rows[index][field_name], scale_from, combined_row[final_field_name])

    combined_row['answer_value'] = answer_value

    return combined_row

def log(data_name, text):
    """ Print debugging output in a consistent way. """
    print(data_name + ": " + text)

def scale(value, inMin, inMax, outMin, outMax, clip=True):
    # TODO This has lots of room for optimisation.

    inRange = inMax - inMin
    outRange = outMax - outMin

    zeroed = value - inMin
    scaled = zeroed / inRange * outRange
    centered = scaled + outMin

    if centered < outMin:
        if clip:
            centered = outMin
        else:
            return False

    if centered > outMax:
        if clip:
            centered = outMax
        else:
            return False

    return centered

def make_variant(source_row, multiplier):
    output_row = {}

    for key in source_row:
        output_row[key] = source_row[key] * multiplier

    return output_row

def make_variants(row):
    output_rows = []

    for multiplier in range(1, 10):
        positive = multiplier / 10

        output_rows.append(make_variant(row, positive))
        output_rows.append(make_variant(row, positive * -1))
    output_rows.append(make_variant(row, -1))

    return output_rows


# Do the initial pass.
root_rows = read_csv(file_name)
row_count = len(root_rows)
root_rows = calculate_diff(root_rows, 'long', 'lat', 'diff', 'angle')
root_rows = calculate_simple_diff(root_rows, 'angleDiff', 'angleDiffDiff')
root_rows = calculate_mean(root_rows, 'diff', 'meanDiff')
root_rows = calculate_simple_diff(root_rows, 'diff', 'diffdiff')
root_rows = calculate_mean(root_rows, 'diffdiff', 'meanDiffdiff')


# Primitive detection of bad points.
for root_index, root_row in enumerate(root_rows):
    root_row['failDirection'] = 0
    root_row['corrected'] = 0
    root_row['mark'] = ''
    root_row['correctedLong'] = root_row['long']
    root_row['correctedLat'] = root_row['lat']

    if root_index == 0:
        continue

    # if root_row['diffdiff'] > threshold:
    #     root_row['failDirection'] = 1
    #
    # if root_row['diffdiff'] < n_threshold_value:
    #     root_row['failDirection'] = -1

    if root_row['angleDiffDiff'] > angle_threshold:
        root_row['failDirection'] = 1

    if root_row['angleDiffDiff'] < n_angle_threshold:
        root_row['failDirection'] = -1

    if root_row['failDirection'] != 0:
        oppositeDirection = root_row['failDirection'] * -1

        # This relies on there being at least two assumptions from above:
        # * root_index == 0 is skipped, which leaves failDirection at 0.
        # * failDirection must not be 0 to get here.
        #
        # If either of these things are no longer true in the future, we may need to test for it.
        if root_rows[root_index - 1]['failDirection'] == oppositeDirection:
            # The error is correctable, and this point is probably not an error.
            root_row['failDirection'] = 0

            pointToCorrect = root_index - 1
            assumedPreviousGoodPoint = root_index - 2
            root_rows[pointToCorrect]['correctedLong'] = (
                float(root_rows[assumedPreviousGoodPoint]['correctedLong']) +
                float(root_row['correctedLong'])) / 2
            root_rows[pointToCorrect]['correctedLat'] = (
                float(root_rows[assumedPreviousGoodPoint]['correctedLat']) +
                float(root_row['correctedLat'])) / 2

            root_rows[pointToCorrect]['mark'] = 'toCorrect'
            root_rows[assumedPreviousGoodPoint]['mark'] = 'previous'
            root_rows[pointToCorrect]['corrected'] = 1
            root_row['corrected'] = 2


# Recalculate stuff.
root_rows = calculate_diff(root_rows, 'correctedLong', 'correctedLat', 'correctedDiff', 'correctedAngle')
# root_rows = calculate_simple_diff(root_rows, 'correctedAngle', 'correctedAngleDiff')
root_rows = calculate_simple_diff(root_rows, 'correctedAngleDiff', 'correctedAngleDiffDiff')
root_rows = calculate_mean(root_rows, 'correctedDiff', 'correctedMeanDiff')
root_rows = calculate_simple_diff(root_rows, 'correctedDiff', 'correctedDiffdiff')
root_rows = calculate_mean(root_rows, 'correctedDiffdiff', 'correctedMeanDiffdiff')

# Do some conversions
angle_conversions = ['angle', 'angleDiff', 'correctedAngle', 'correctedAngleDiff']
# Expected to be used is src_field + 'IntPositiveCentered'. Eg 'angleIntPositiveCentered'.
for src_field in angle_conversions:
    root_rows = to_int_degrees(root_rows, src_field, src_field + 'Int', 360, int(255/2))

distance_conversions = ['diff', 'diffdiff', 'correctedDiff', 'correctedDiffdiff']
# Expected to be used is src_field + 'ScaledInt'. Eg diffScaledInt.
for src_field in distance_conversions:
    root_rows = to_int_distance(root_rows, src_field, src_field + 'ScaledInt', 0.003, int(255/2))

# Write out the basic stuff.
log(name, "Write main CSV.")
write_csv(destination_file, root_rows)

if create_float_graph:
    log(name, "Write main graphs. - Float")
    create_generic_graph(
        destination_graph_file_image,
        destination_graph_file_pdf,
        name + ' - Float values',
        'Distance',
        [
            'diffdiff',
            'correctedDiffdiff',
            'diff',
            'correctedDiff'
        ],
        'Angle (Radians)',
        [
            'angleDiff',
            'correctedAngleDiff'
        ],
        root_rows,
        threshold)

if create_centered_graph:
    log(name, "Write main graphs. - Int centered")
    create_generic_graph(
        destination_graph_file_image + 'IntCentered',
        destination_graph_file_pdf + 'IntCentered',
        name + ' - Integer centered',
        'Quantised',
        [
            'angleDiffIntPositiveCentered',
            'correctedAngleDiffIntPositiveCentered',
            'diffdiffScaledIntCentered',
            'correctedDiffdiffScaledIntCentered',
            # 'angleDiffIntPositiveCenteredN',
            # 'correctedAngleDiffIntPositiveCenteredN',
            # 'diffdiffScaledIntCenteredN',
            # 'correctedDiffdiffScaledIntCenteredN'
        ],
        'Empty',
        [],
        root_rows)

if create_signed_graph:
    log(name, "Write main graphs. - Int signed")
    create_generic_graph(
        destination_graph_file_image + 'IntSigned',
        destination_graph_file_pdf + 'IntSigned',
        name + ' - Integer signed',
        'Quantised',
        [
            'angleDiffInt',
            'correctedAngleDiffInt',
            'diffScaledInt',
            'correctedDiffScaledInt',
            # 'angleDiffIntN',
            # 'correctedAngleDiffIntN',
            # 'diffScaledIntN',
            # 'correctedDiffScaledIntN'
        ],
        'Empty',
        [],
        root_rows)


# Take just what we need.
log(name, "Take just what we need.")
concise_rows = []
for root_index, root_row in enumerate(root_rows):
    new_row = {}
    for fieldIndex, requested_field in enumerate(fields_to_take):
        new_row[requested_field] = root_row[requested_field]

    concise_rows.append(new_row)

# Extract samples.
log(name, "Extract samples:")
threshold = sample_size - 1
clean_rows = 0
dirty_rows = 0
accumulated_rows = 0
clean_samples = 0
dirty_samples = 0
non_viable_samples = 0
oob = False
binary_rows = {
    "A" : [], # Training data. (Mix of good and not good.)
    "B" : [], # Testing data. (Mix of good and not good.)
    "C" : []  # Discarded data (excess clean data).
    }
angle_rows = {
    "A" : [], # Training data. (All good data.)
    "B" : [], # Testing data. (All good data.)
    "C" : []  # Non-good data.
    }
print(name + ': ', end='')

for root_index, root_row in enumerate(root_rows):
    root_good = root_row['failDirection'] == 0
    cleanEnough = (root_good or root_row['corrected'] != 0)

    # Track how good the previous samples have been.
    accumulated_rows += 1
    if root_good:
        clean_rows += 1
        dirty_rows = 0
    else:
        # If we have enougn samples, and only the last one is broken, we still want it.
        clean_rows = 0
        dirty_rows += 1

    if accumulated_rows < sample_size:
        # We don't have enough samples.
        print(' ', end='', flush=True)
        non_viable_samples += 1

        if not root_good:
            accumulated_rows = 0

        continue

    if not root_good:
        accumulated_rows = 0

    # Choose destination.
    if root_good:
        print('+', end='', flush=True)
        clean_samples += 1
        sample_destination = destination_samples_clean
        sample_graph_destination = destination_samples_graph_clean
    else:
        print('-', end='', flush=True)
        dirty_samples += 1
        sample_destination = destination_samples_dirty
        sample_graph_destination = destination_samples_graph_dirty

    # Collect the relevant samples.
    relevant_samples = []
    start_pos = root_index - sample_size + 1
    end_pos = root_index + 1
    for relevantIndex in range(start_pos, end_pos):
        relevant_samples.append(concise_rows[relevantIndex])

    # Create binary rows for later use.
    if len(binary_rows['A']) * ab_split_negative < len(binary_rows['B']) * ab_split:
        group = "A"
    else:
        group = "B"

    if cleanEnough:
        should_add = (not root_good) # Always add the cleanEnough bad ones.
        if root_index % sample_size == 0:
            # Always add a cleanEnough sample regardless if it's 1 in every sample_size samples.
            should_add = True

        if not should_add:
            # Collect excluded items in group C.
            group = "C"

        binary_row = rows_to_binary_row(relevant_samples, combined_binary_fields_to_take, root_good)
        binary_rows[group].append(binary_row)

    # Create angle rows for later use.
    if len(angle_rows['A']) * ab_split_negative < len(angle_rows['B']) * ab_split:
        group = "A"
    else:
        group = "B"

    if not root_good:
        group = "C"

    # TODO Make this better.
    # answer = int(root_row['angleDiff'] * 1)
    # answer = root_row['angleDiff'] * 1000
    # if answer > 100: answer = 100
    # if answer < -100: answer = -100

    # if answer > cutOff: group = "C"
    # if answer < nCutOff: group = "C"
    # answer += 100
    # answer /= 100

    answer = scale(root_row['angleDiff'], nUnScaled, unScaled, 0.01, 0.99)
    if answer is False :
        group = "C"
        answer = root_row['angleDiff']
        oob = True

    for angle_row in relevant_samples:
        if answer > angleCutoff:
            group = "C"
        if answer < nAngleCutoff:
            group = "C"

    angle_row = rows_to_angle_row_scale(relevant_samples, combined_angle_fields_to_take, angle_base, angle_base, answer)
    angle_rows[group].append(angle_row)

    # Give some more variety to our training data.
    # variants = make_variants(angle_row)
    # for variant in variants:
    #     angle_rows[group].append(variant)

    # Write out data.
    sample_name = name + '-' + str(start_pos) + '-' + str(end_pos)
    file_name = sample_destination + '/' + sample_name + '-' + group
    file_csv = file_name + '.csv'
    write_csv(file_csv, relevant_samples)

    # Create a simple graph of this data.
    if create_sample_graphs:
        create_generic_graph(
            file_name,
            file_name,
            'Sample: ' + sample_name,
            'Quantised',
            [
                'angleDiffInt',
                'correctedAngleDiffInt',
                'diffScaledInt',
                'correctedDiffScaledInt'
            ],
            'Unknown',
            [],
            relevant_samples,
            create_pdf=False)

    # Reset tracking of good samples.
    if not cleanEnough:
        clean_rows = 0
        continue
print()

# Write binary data.
log(name, "Write binary data.")
for _, set_name in enumerate(binary_rows):
    file_name = destination_samples_binary + '/' + set_name + '/' + name
    file_csv = file_name + '.csv'
    write_csv(file_csv, binary_rows[set_name])

# Graph angle data.
if create_normalised_angles_graph:
    create_generic_graph(
        destination_graph_file_image + 'FloatAngles',
        destination_graph_file_pdf + 'FloatAngles',
        name + ' - Angles ready for consumption',
        'Angles',
        angle_rows['A'][1].keys(),
        'Empty',
        [],
        angle_rows['A'],
        create_pdf=True)

# Write angle data.
log(name, "Write angle data.")
for _, set_name in enumerate(angle_rows):
    file_name = destination_samples_binary + '/angle' + set_name + '/' + name
    file_csv = file_name + '.csv'
    write_csv(file_csv, angle_rows[set_name])

print(f"{name}: Eligible clean samples: {clean_samples}   Eligible dirty samples: {dirty_samples}   Non-viable samples: {non_viable_samples}")
