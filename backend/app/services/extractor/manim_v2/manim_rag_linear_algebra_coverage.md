# Manim RAG Linear Algebra Coverage

Status legend:
- `DONE` rewritten as a ManimCE example and render-verified
- `TODO` source file is in scope but not yet mined
- `PARTIAL` source file has at least one rewritten example, but mining is not complete
- `SKIP` intentionally omitted because the file is title-card / thumbnail / duplicate-heavy / low pedagogical yield

## Source scope

- `../3b1b-videos/_2015/matrix_as_transform_2d.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter0.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter1.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter2.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter3.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter4.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter5.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter6.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter7.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter8.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter8p2.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter9.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter10.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/chapter11.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/footnote.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/footnote2.py` - `PARTIAL`
- `../3b1b-videos/_2016/eola/thumbnails.py` - `SKIP`
- `../3b1b-videos/_2018/cramer.py` - `PARTIAL`
- `../3b1b-videos/_2018/determinant_puzzle.py` - `PARTIAL`
- `../3b1b-videos/_2021/quick_eigen.py` - `PARTIAL`
- `../3b1b-videos/_2021/matrix_exp.py` - `PARTIAL`

## Rewritten examples

- `DONE` `columns_to_basis_vectors`
  source: `3b1b/_2016/eola/chapter3.py::ColumnsToBasisVectors`
  note: core column picture for matrix actions; render-verified at `-ql`

- `DONE` `linear_combinations_span_plane`
  source: `3b1b/_2016/eola/chapter2.py::ShowVaryingLinearCombinations+AnimationUnderSpanDefinition`
  note: non-parallel vectors and span via live coefficients and sampled endpoints

- `DONE` `dependent_vectors_span_line`
  source: `3b1b/_2016/eola/chapter2.py::LinearDependentVectors+WhenVectorsLineUp`
  note: dependence collapse to a line; render-verified at `-ql`

- `DONE` `coordinates_as_scalars`
  source: `3b1b/_2016/eola/chapter2.py::CoordinatesAsScalars`
  note: coordinates as live scalar weights on basis vectors

- `DONE` `composition_rotation_then_shear`
  source: `3b1b/_2016/eola/chapter4.py::RotationThenShear+IntroduceIdeaOfComposition`
  note: order-sensitive composition with explicit `S(Rx) = (SR)x`

- `DONE` `matrix_multiplication_noncommutative`
  source: `3b1b/_2016/eola/chapter4.py::FirstShearThenRotation+RotationThenShear+AskAboutCommutativity`
  note: side-by-side transforms show `SR != RS`

- `DONE` `determinant_area_scaling`
  source: `3b1b/_2016/eola/chapter5.py::DiagonalExampleWithSquare+NameDeterminant`
  note: determinant as area scaling of the unit square

- `DONE` `determinant_ad_minus_bc`
  source: `3b1b/_2016/eola/chapter5.py::TwoDDeterminantFormulaIntuition+FullFormulaExplanation`
  note: live parallelogram area tied to the formula `ad-bc`

- `DONE` `dot_product_as_projection`
  source: `3b1b/_2016/eola/chapter7.py::GeometricInterpretation+GeometricInterpretationNegative`
  note: signed projection interpretation with positive-to-negative sweep

- `DONE` `inverse_transformation_undoes_action`
  source: `3b1b/_2016/eola/chapter6.py::DescribeInverse+PlayInReverse`
  note: inverse map shown as geometric undo for `Ax = v`

- `DONE` `change_of_basis_same_vector`
  source: `3b1b/_2016/eola/chapter9.py::JennysGrid+ChangeOfBasisExample`
  note: same vector, different coordinates under a new basis

- `DONE` `change_basis_matrix_columns`
  source: `3b1b/_2016/eola/chapter9.py::TalkThroughChangeOfBasisMatrix+ChangeOfBasisExample`
  note: change-of-basis matrix columns are the new basis vectors in standard coordinates

- `DONE` `eigenvector_invariant_line`
  source: `3b1b/_2016/eola/chapter10.py::VectorRemainsOnSpan+SneakierEigenVector`
  note: eigenvector/eigenspace invariance contrasted with a generic vector

- `DONE` `rotation_matrix_powers_cycle`
  source: `3b1b/_2021/matrix_exp.py::Show90DegreePowers`
  note: quarter-turn matrix powers cycle with `R^4 = I`

- `DONE` `diagonal_eigenbasis_repeated_powers`
  source: `3b1b/_2016/eola/chapter10.py::BasisVectorsAreEigenvectors+DefineDiagonalMatrix+RepeatedMultiplicationInAction`
  note: eigenbasis makes repeated powers independent scalar growth/decay

- `DONE` `matrix_exponential_rotation_flow`
  source: `3b1b/_2021/matrix_exp.py::CircularPhaseFlow+CircularFlowEvaluation+HowExampleLeadsToMatrixExponents`
  note: `e^{tJ}` shown as continuous circular flow for a linear ODE

- `DONE` `two_d_cross_product_signed_area`
  source: `3b1b/_2016/eola/chapter8.py::Define2dCrossProduct+show_sign`
  note: signed 2D cross product as live parallelogram area and orientation

- `DONE` `cramers_rule_area_ratio`
  source: `3b1b/_2018/cramer.py::ThinkOfPuzzleAsLinearCombination+WriteCramersRule`
  note: Cramer's rule as ratio of determinant-defined areas

- `DONE` `vector_addition_head_to_tail`
  source: `3b1b/_2016/eola/chapter1.py::VectorAddition+VectorAdditionNumerically`
  note: head-to-tail vector addition with matching coordinate sum

- `DONE` `scalar_multiplication_direction_flip`
  source: `3b1b/_2016/eola/chapter1.py::ShowScalarMultiplication+ScalingNumerically`
  note: scalar multiplication as stretch / shrink / direction flip

- `DONE` `linearity_additivity`
  source: `3b1b/_2016/eola/chapter6.py::ShowAdditivityProperty`
  note: geometric proof that `A(v+w)=Av+Aw`

- `DONE` `origin_fixed_linear_transform`
  source: `3b1b/_2016/eola/chapter3.py::MovingOrigin+IntroduceLinearTransformations`
  note: contrasts a linear shear fixing the origin with a translated grid

- `DONE` `homogeneity_scaling_property`
  source: `3b1b/_2016/eola/chapter3.py::PrepareForFormalDefinition+chapter11.py::FormalDefinitionOfLinear`
  note: scaling before or after a linear map gives `A(c v)=c A v`

- `DONE` `determinant_orientation_flip`
  source: `3b1b/_2016/eola/chapter5.py::NegativeDeterminant+FlipSpaceOver`
  note: negative determinant means orientation reversal, not negative area size

- `DONE` `rank_is_output_dimension`
  source: `3b1b/_2016/eola/chapter6.py::DefineRank+ShowVInAndOutOfColumnSpace`
  note: side-by-side rank 2 vs rank 1 output spaces

- `DONE` `column_space_null_space`
  source: `3b1b/_2016/eola/chapter6.py::DefineColumnSpace+NameNullSpace+OffsetNullSpace`
  note: null-space offsets collapse to the same output on the column space

- `DONE` `eigen_directions_stretch_unit_disk`
  source: `3b1b/_2021/quick_eigen.py::ShowSquishingAndStretching`
  note: eigen-directions stay fixed while the unit disk stretches and shrinks

- `DONE` `rotation_no_real_eigenvectors`
  source: `3b1b/_2016/eola/chapter10.py::ThereMightNotBeEigenvectors+Rotate90Degrees`
  note: 90-degree rotation knocks every nonzero real vector off its span

- `DONE` `zero_determinant_many_or_none`
  source: `3b1b/_2018/cramer.py::ShowZeroDeterminantCase`
  note: singular maps collapse many inputs to one output and miss off-line targets

- `DONE` `linear_vs_nonlinear_grid`
  source: `3b1b/_2015/matrix_as_transform_2d.py::ExamplesOfNonlinearTwoDimensionalTransformations`
  note: linear shear preserves straight grid lines while a nonlinear warp bends them

- `DONE` `matrix_vector_numeric_geometric`
  source: `3b1b/_2016/eola/chapter0.py::NumericVsGeometric+ExampleTransformation`
  note: matrix-vector multiplication shown both as arithmetic and as a plane action

- `DONE` `dot_product_dual_transform`
  source: `3b1b/_2016/eola/chapter8p2.py::DotProductToTransformSymbol+DefineDualTransform`
  note: fixed-vector dot product as a live 2D-to-1D row-matrix transformation

- `DONE` `polynomial_coordinates_basis`
  source: `3b1b/_2016/eola/chapter11.py::GeneneralPolynomialCoordinates+IntroducePolynomialSpace`
  note: polynomial coefficients as coordinates in the basis `1, x, x^2, ...`

- `DONE` `derivative_linear_operator`
  source: `3b1b/_2016/eola/chapter11.py::DerivativeIsLinear`
  note: derivative as a linear operator on function space

- `DONE` `determinant_product_successive`
  source: `3b1b/_2018/determinant_puzzle.py::SuccessiveLinearTransformations`
  note: successive area scaling explains `det(M_1M_2)=det(M_1)det(M_2)`

- `DONE` `three_d_basis_columns_matrix`
  source: `3b1b/_2016/eola/footnote.py::PutTogether3x3Matrix+TransformOnlyBasisVectors`
  note: 3D matrix columns record transformed basis vectors

- `DONE` `nonsquare_matrix_dimension_map`
  source: `3b1b/_2016/eola/footnote2.py::Symbolic2To1DTransform+TwoDTo1DTransform`
  note: non-square row matrix maps a 2D vector to a 1D number-line output

## Planned topic buckets

- vectors and coordinates: geometric vector, coordinates as scalars, basis choice
- span and basis: linear combinations, spanning line vs plane, dependence, basis definition
- linear transformations: moving the grid, additivity, homogeneity, basis-vector control
- matrix mechanics: matrix-vector multiplication, composition, inverse viewpoint
- determinant: area scaling, orientation flip, determinant as signed area
- solving systems: inverse transform intuition, Cramer's rule, zero-determinant failure
- dot and cross: projection, dual view, 2D cross product / area
- change of basis: alternate grids and coordinate systems
- eigenstuff: invariant lines, eigenvalue scaling, characteristic intuition
- matrix exponential: repeated action, powers, continuous-time linear dynamics

## QA notes

- `2026-04-25` optimized dynamic vector arrows across LA scenes to use fixed-size `Line.add_tip` arrowheads where the endpoint changes over time; verified no `always_redraw(lambda: Arrow(...))` remains in `examples/linear_algebra`.
- `2026-04-25` full LA quality gate: `py_compile` passed for all 37 scene files and `manim -ql --disable_caching` rendered all 37 scenes successfully.
